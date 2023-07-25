import os
import time
import numpy
import random
from PIL import Image
from config import Config
from pyrogram import filters
from translation import Translation
from database.access import clinton
from database.adduser import AddUser
from pyrogram import Client as Clinton
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helper_funcs.help_Nekmo_ffmpeg import take_screen_shot

@Clinton.on_message(filters.private & filters.photo)
async def save_photo(bot, update):
    await AddUser(bot, update)
    await clinton.set_thumbnail(update.from_user.id, thumbnail=update.photo.file_id)
    await bot.send_message(chat_id=update.chat.id, text=Translation.SAVED_CUSTOM_THUMB_NAIL, reply_to_message_id=update.message_id)

@Clinton.on_message(filters.private & filters.command("delthumbnail"))
async def delthumbnail(bot, update):
    await AddUser(bot, update)
    await clinton.set_thumbnail(update.from_user.id, thumbnail=None)
    await bot.send_message(chat_id=update.chat.id, text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL, reply_to_message_id=update.message_id)

@Clinton.on_message(filters.private & filters.command("viewthumbnail") )
async def viewthumbnail(bot, update):
    await AddUser(bot, update)
    thumbnail = await clinton.get_thumbnail(update.from_user.id)
    if thumbnail is not None:
        await bot.send_photo(
        chat_id=update.chat.id,
        photo=thumbnail,
        caption=f"Your current saved thumbnail 🦠",
        reply_to_message_id=update.message_id)
    else:
        await update.reply_text(text=f"No Thumbnail found 🤒")

async def Gthumb01(bot, update):
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await clinton.get_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
        Image.open(thumbnail).convert("RGB").save(thumbnail)
        img = Image.open(thumbnail)
        img.resize((100, 100))
        img.save(thumbnail, "JPEG")
    else:
        thumbnail = None

    return thumbnail

async def Gthumb02(bot, update, duration, download_directory):
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await clinton.get_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
    else:
        thumbnail = await take_screen_shot(download_directory, os.path.dirname(download_directory), random.randint(0, duration - 1))

    return thumbnail

async def Mdata01(download_directory):
    width = 0
    height = 0
    duration = 0
    metadata = extractMetadata(createParser(download_directory))
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")

    return width, height, duration

async def Mdata02(download_directory):
    width = 0
    duration = 0
    metadata = extractMetadata(createParser(download_directory))
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if metadata.has("width"):
            width = metadata.get("width")

    return width, duration

async def Mdata03(download_directory):
    duration = 0
    metadata = extractMetadata(createParser(download_directory))
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds

    return duration

async def get_flocation(download_directory, extension):
    try:
        file_size = os.stat(download_directory).st_size
        return file_size, download_directory
    except Exception:
        pass
    try:
        file_directory = download_directory + ".mkv"
        file_size = os.stat(file_directory).st_size
        return file_size, file_directory
    except Exception:
        pass
    try:
        file_directory = download_directory + "." + extension
        file_size = os.stat(file_directory).st_size
        return file_size, file_directory
    except Exception:
        pass
    try:
        file_directory = os.path.splitext(download_directory)[0] + ".mkv"
        file_size = os.stat(file_directory).st_size
        return file_size, file_directory
    except Exception:
        pass
    try:
        file_directory = os.path.splitext(download_directory)[0] + "." + extension
        file_size = os.stat(file_directory).st_size
        return file_size, download_directory
    except Exception:
        return 0, file_directory
