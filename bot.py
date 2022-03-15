from asyncio import events
import ast
import asyncio
import json
from FastTelethonhelper import fast_upload
import mangaSeeFunctions as manga
from config import bot, DATABASE, CHANNEL_ID
from telethon import events
import os


async def get_data():
    db = await bot.get_messages(CHANNEL_ID,ids=DATABASE)
    d = await bot.download_file(db.media)
    data = json.loads(d)
    return data



@bot.on(events.NewMessage(pattern="/checkupdates"))
async def refresh(event):
    try:
        msg = await bot.send_message(event.chat_id,"checking for updates...")
        data = await get_data()
        updates = manga.check_updates(data)
        if updates == []:
            await bot.edit_message(event.chat_id,msg,"No Updates Found :(")
            return
        message = "New Updates Found\n"
        for update in updates:
            message = message + "\n" + update[0] + ": " + str(update[1])
        await bot.edit_message(event.chat_id,msg,str(message))
    except Exception as e:
        print(e)
        await bot.send_message(event.chat_id,f"Following error occured\n\n{str(e)}")

@bot.on(events.NewMessage(pattern="/add"))
async def add_manga(event):
    try:
        txt = event.raw_text.split()
        txt.pop(0)
        txt = "".join(txt)
        txt = txt.split(":")
        print(len(txt))
        if len(txt) >= 3 or len(txt) < 2:
            await bot.send_message(event.chat_id,"Invalid Syntax!, /add accepts only 2 variables mangaid:latest_chapter")
            return
        d = await get_data()
        d[txt[0]] = int(txt[1])
        await manga.update_data(d)
        await bot.send_message(event.chat_id,f"added {txt[0]} to database")
    except Exception as e:
        await bot.send_message(event.chat_id,f"Following error occured\n\n{str(e)}")

@bot.on(events.NewMessage(pattern="/updateall"))
async def update_all(event):
    try:
        data = await get_data()
        await manga.update_all(event,data)
        await bot.send_message(event.chat_id,"Updates Done!")
    except Exception as e:
        await bot.send_message(event.chat_id,f"Following error occured\n\n{str(e)}")



@bot.on(events.NewMessage(pattern="/download"))
async def download_one_chapter(event):
    try:
        txt = event.raw_text.split()
        txt.pop(0)
        txt = "".join(txt)
        txt = txt.split(":")
        print(txt)
        mangaid = txt[0]
        ch = txt[1]
        ch = int(ch)
        a = await bot.send_message(event.chat_id,"downloading...")
        await manga.download_manga_by_chapter(mangaid,ch)
        await a.delete()
        await manga.upload_pdf(event)
    except Exception as e:
        await bot.send_message(event.chat_id,f"Following error occured while downloading {mangaid}-{ch}\n\n{str(e)}")

@bot.on(events.NewMessage(pattern="/batch"))
async def batch_download(event):
    try:
        txt = event.raw_text.split()
        txt.pop(0)
        txt = "".join(txt)
        txt = txt.split(":")
        print(len(txt))
        print(txt)
        mangaid = txt[0]
        ch_start = int(txt[1])
        ch_end = int(txt[2])
        print([mangaid,ch_start,ch_end])
        await manga.dowload_batch_chapters(event=event,mangaid=mangaid,ch_start=ch_start,ch_end=ch_end)
    except Exception as e:
        await bot.send_message(event.chat_id,f"Following error occured \n\n{str(e)}")

@bot.on(events.NewMessage(pattern="/remove"))
async def remove(event):
    try:
        txt = event.raw_text.split()
        txt = txt[-1]
        print(txt)
        db = await get_data()
        db.pop(txt)
        await manga.update_data(db)
        await bot.send_message(event.chat_id,f"removed {txt} from database")
    except KeyError:
        await bot.send_message(event.chat_id,"dataset does not exist")
    except Exception as e:
        await bot.send_message(event.chat_id,f"Following error occured\n\n{str(e)}")

@bot.on(events.NewMessage(pattern="/backup"))
async def backup(event):
    try:
        data = await get_data()
        backup = json.dumps(data,indent=4)
        with open("backup.json","w") as f:
            f.write(backup)
        await bot.send_file(event.chat_id,"backup.json")
        os.remove("backup.json")
    except Exception as e:
        await bot.send_message(event.chat_id,f"Following error occured\n\n{str(e)}")


@bot.on(events.NewMessage(pattern="/restore"))
async def restore(event):
    try:
        x = await event.get_reply_message()
        backup = await bot.download_file(x.media)
        data = json.loads(backup)
        await manga.update_data(data)
        await bot.send_message(event.chat_id,"data restored!")
    except Exception as e:
        await bot.send_message(event.chat_id,f"Following error occured\n\n{str(e)}")


@bot.on(events.NewMessage(pattern="/show"))
async def show_data(event):
    try:
        data = await get_data()
        data = json.dumps(data,indent=2)
        await bot.send_message(event.chat_id,str(data))
    except Exception as e:
        await bot.send_message(event.chat_id,f"Following error occured\n\n{str(e)}")



bot.start()
bot.run_until_disconnected()

