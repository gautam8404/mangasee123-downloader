from fileinput import filename
import shutil
import img2pdf
import MangaseeDL as manga
import os
from FastTelethonhelper import fast_upload
from config import CHANNEL_ID, DATABASE
from config import bot
import json



async def get_data():
    db = await bot.get_messages(CHANNEL_ID,ids=DATABASE)
    d = await bot.download_file(db.media)
    data = json.loads(d)
    return data

async def update_data(data):
    update = json.dumps(data,indent=4)
    file = "database.json"
    with open(file,"w") as f:
            f.write(update)
    x =  await bot.get_messages(CHANNEL_ID,ids=DATABASE)
    await bot.edit_message(CHANNEL_ID,x,file=file,force_document=True)
    os.remove(file)

async def upload_pdf(event):
    r = await bot.send_message(event.chat_id,"uploading...")
    f = os.listdir("pdfs/")[0]
    x = await fast_upload(client=bot,file_location=f"pdfs/{f}",reply=r)
    await bot.send_file(event.chat_id,x,force_document=True)
    await r.delete()


def convert_to_pdf(name):
    print(name)
    pages = os.listdir("images/")
    prefix = "images/"
    imgs = [prefix + x for x in pages]
    imgs = sorted(imgs)
    with open(f"pdfs/{name}.pdf", "wb") as f:
        f.write(img2pdf.convert(imgs))

def delete_files(dir):  
    folder = dir
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

async def download_manga_by_chapter(mangaid,chapter):
    delete_files("images/")
    delete_files("pdfs/")
    ch = manga.get_manga_details(mangaid)
    target_ch = [ch[chapter]]
    await manga.download_chapters(mangaid,target_ch)
    name = f"{mangaid} {chapter}"
    convert_to_pdf(name)

def get_latest_chapter(mangaid):
    chapters = manga.get_manga_details(mangaid)
    latest_chapter = list(chapters.keys())[-1]
    return latest_chapter

async def download_latest_chapter(mangaid):
    target = get_latest_chapter(mangaid)
    await download_manga_by_chapter(mangaid,target)


async def dowload_batch_chapters(event, mangaid,ch_start,ch_end):
    chapters_dict = manga.get_manga_details(mangaid)
    for ch in range(ch_start, ch_end + 1):
        try:
            chapter = chapters_dict.get(ch)
            if not chapter:
                print(f"Chapter {ch} is not available, skipping...")
            else:
                a = await bot.send_message(event.chat_id,f"Downloading {mangaid} chapter {ch}")
                await download_manga_by_chapter(mangaid,ch)
                await a.delete()
                await upload_pdf(event)
        except Exception as e:
            await bot.send_message(event.chat_id,f"Following error occured while downloading {mangaid}-{ch}\n\n{str(e)}")


def check_updates(data):
    updates = []
    temp_database = dict(data)
    for i in temp_database:
        c = temp_database.get(i)
        ch = int(c)
        a = get_latest_chapter(i)
        a = int(a)
        print(ch)
        if ch>= a:
            continue
        else:
            for z in range(ch+1,a + 1):
                updates.append([i,z])
    return updates



async def update_all(event,data):
    updates = check_updates(data)
    for update in updates:
        try:
            x = await bot.send_message(event.chat_id,f"Downloading {update[0]}: {update[1]}")
            await download_manga_by_chapter(update[0],update[1])
            await x.delete()
            a = os.listdir("pdfs/")
            await upload_pdf(event)
            db_dict = await get_data()
            db_dict[update[0]] = update[1]
            await update_data(db_dict)
        except Exception as e:
            await bot.send_message(event.chat_id,f"Following error ocuured while downloading {update[0]}: {update[1][0]}\n\n {str(e)}")
