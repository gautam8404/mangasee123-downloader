import asyncio
import json
import os
import re
import sys
from typing import Iterable
import cloudscraper
import aiofiles
import aiohttp
import requests
import shutil
import img2pdf
MANGASEE123HOST = "https://mangasee123.com"


def remove_leading_zeros(num: str) -> str:
    """
    Remove leading zeros from a string.
    """
    num = str(num)
    first_non_zero_index = 0

    for i, c in enumerate(num):
        if c != "0":
            first_non_zero_index = i
            break

    return num[first_non_zero_index:]


def add_leading_zeros(num: str, total_len: int) -> str:
    """
    Add leading zeros to a string to reach the specified length.
    """
    num = str(num)
    needed_zeros = total_len - len(num)

    if needed_zeros > 0:
        return "0" * needed_zeros + num

    return num


def get_chapter_first_page_url(manga_name: str, chapter: str, page: str):
    """
    Get mangasee123 reader url for a specific manga/chapter/page

    Boch chapter and page should be without leading zeros
    """
    return (
        f"{MANGASEE123HOST}/read-online/{manga_name}-chapter-{chapter}-page-{page}.html"
    )


def get_page_image_url(host, name, chapter, page):
    """
    Get hosted image url for a specific manga page
    """

    chapter = add_leading_zeros(chapter, 4)
    page = add_leading_zeros(page, 3)
    return f"https://{host}/manga/{name}/{chapter}-{page}.png"


def get_manga_details(name):
    """
    Get details for a manga from Mangasee123.
    Details include available chapters and number of pages in each chapter
    """
    print(name)
    url = get_chapter_first_page_url(name, "1", "1")
    scraper = cloudscraper.create_scraper()
    # resp = requests.get(url)
    resp = scraper.get(url)
    # print(url)
    content = resp.content.decode("utf-8")
    # print(content)
    chapter_details_pattern = re.compile("vm.CHAPTERS = (.*);")
    chapter_details_str = chapter_details_pattern.search(content).groups()[0]
    chapter_details_list = json.loads(chapter_details_str)

    chapter_details_dict = {}
    for chapter_detail in chapter_details_list:
        chapter_details_dict[
            int(remove_leading_zeros(chapter_detail["Chapter"][1:-1]))
        ] = chapter_detail

    return chapter_details_dict


async def get_chapter_download_and_save_data(
    session, name: str, chapter: int, pages: int
) -> list:
    """
    Specify the url and save path for each page of a chapter
    """
    data = []

    url = get_chapter_first_page_url(name, chapter, 1)

    # resp = await session.request(method="GET", url=url)
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url)
    content = resp.text
    host_pattern = re.compile('vm.CurPathName = "(.*)";')
    host = host_pattern.search(content).groups()[0]

    for page in range(1, int(pages) + 1):
        page = add_leading_zeros(page, 3)
        download_url = get_page_image_url(host, name, chapter, page)
        save_path = os.path.join("images", f"{page}.jpg")

        data.append({"download_url": download_url, "save_path": save_path})

    return data

async def download_and_save_chapter(session: aiohttp.ClientSession, name, chapter, pages):
    """
    Asynchronously download and save a page (skip if file exists)
    """
    try:
        print(f"Started downloading chapter {chapter}...")
        data = await get_chapter_download_and_save_data(session, name, chapter, pages)

        for d in data:
            download_url = d["download_url"]
            save_path = d["save_path"]

            # ! UNCHECK BEFORE PUSHING
            if os.path.isfile(save_path):
                continue 

            scraper = cloudscraper.create_scraper()
            # resp = await session.request(method="GET", url=download_url)
            resp = scraper.get(download_url)
            async with aiofiles.open(save_path, "wb") as f:
                await f.write(resp.content)
        print(f"Finished downloading chapter {chapter}...")
    except asyncio.TimeoutError:
        print(f"Timeout in downloading chapter {chapter}!")


async def download_chapters(name: str, chapter_details: Iterable):
    """
    Main couroutine for downloading chapters
    """
    if os.path.isfile(name):
        raise FileExistsError


    async with aiohttp.ClientSession() as session:
        print("Fetching requested chapter details...")

        coroutines = []
        for ch_detail in chapter_details:
            chapter = ch_detail["Chapter"][1:-1]
            pages = int(ch_detail["Page"])

            coroutines.append(
                download_and_save_chapter(session, name, chapter, pages),
            )

        print(f"Downloading requested chapters...")
        await asyncio.gather(*coroutines)
        print("Download completed!")


