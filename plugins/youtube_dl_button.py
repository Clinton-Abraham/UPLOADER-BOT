import os
import json
import math
import time
import shutil
import asyncio
from PIL import Image
from config import Config
from datetime import datetime
from database.access import clinton
from translation import Translation
from plugins.custom_thumbnail import *
from pyrogram.types import InputMediaPhoto
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes

async def youtube_dl_call_back(bot, update):
    try:
        cb_data = update.data
        tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("|")
        save_ytdl_json_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".json"
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except Exception:
        await update.message.delete(True)
        return
    youtube_dl_url = update.message.reply_to_message.text
    custom_file_name = str(response_json.get("title"))[:50] + "_" + youtube_dl_format
    youtube_dl_username = None
    youtube_dl_password = None
    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        elif len(url_parts) == 4:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in update.message.reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + l]
        if youtube_dl_url is not None:
            youtube_dl_url = youtube_dl_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
    else:
        for entity in update.message.reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                youtube_dl_url = youtube_dl_url[o:o + l]

    await update.message.edit(text=Translation.DOWNLOAD_START)
    description = Translation.CUSTOM_CAPTION_UL_FILE
    if "fulltitle" in response_json:
        description = response_json["fulltitle"][0:1021]
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    if '/' in custom_file_name:
        file_mimx = custom_file_name
        file_maix = file_mimx.split('/')
        file_name = ' '.join(file_maix)
    else:
        file_name = custom_file_name

    command_to_exec = []
    command_to_exec.append("--quiet")
    command_to_exec.append("--no-warnings")
    download_directory = tmp_directory_for_each_user + "/" + str(file_name) + "." + youtube_dl_ext
    if tg_send_type == "audio":
        command_to_exec = ["yt-dlp", "-c",
        "--prefer-ffmpeg", "--extract-audio",
        "--audio-format", youtube_dl_ext,
        "--audio-quality", youtube_dl_format,
        youtube_dl_url, "-o", download_directory]
    else:
        minus_f_format = youtube_dl_format
        if "youtu" in youtube_dl_url:
            minus_f_format = youtube_dl_format + "+bestaudio"
        command_to_exec = ["yt-dlp", "-c",
        "--embed-subs", "-f", minus_f_format,
        "--hls-prefer-ffmpeg", youtube_dl_url,
        "-o", download_directory]

    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)

    start = datetime.now()
    asyncio.create_task(clendir(save_ytdl_json_path))
    process = await asyncio.create_subprocess_exec(*command_to_exec,
    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if e_response:
        await bot.edit_message_text(chat_id=update.message.chat.id,
        message_id=update.message.message_id, text="ERROR : Download failed ⚠️")
        return
    if not t_response:
        asyncio.create_task(clendir(tmp_directory_for_each_user))
        await bot.edit_message_text(chat_id=update.message.chat.id,
        text="ERROR : File not found 😑", message_id=update.message.message_id)
        return
    file_size, file_location = await get_flocation(download_directory, youtube_dl_ext)
    if file_size == 0:
        await update.message.edit(text="ERROR : File Not found 🙁")
        asyncio.create_task(clendir(tmp_directory_for_each_user))
        return
    await update.message.edit(text=Translation.UPLOAD_START)
    try:
        start_time = time.time()
        if tg_send_type == "audio":
            duration = await Mdata03(file_location)
            thumbnail = await Gthumb01(bot, update)
            await bot.send_audio(
            chat_id=update.message.chat.id,
            audio=file_location,
            caption=description,
            parse_mode="HTML",
            duration=duration,
            thumb=thumbnail,
            reply_to_message_id=update.message.reply_to_message.message_id,
            progress=progress_for_pyrogram,
            progress_args=(Translation.UPLOAD_START, update.message, start_time))
        elif tg_send_type == "file":
            thumbnail = await Gthumb01(bot, update)
            await bot.send_document(chat_id=update.message.chat.id,
            document=file_location,
            thumb=thumbnail,
            caption=description,
            parse_mode="HTML",
            reply_to_message_id=update.message.reply_to_message.message_id,
            progress=progress_for_pyrogram,
            progress_args=(Translation.UPLOAD_START, update.message, start_time))
        elif tg_send_type == "vm":
            width, duration = await Mdata02(file_location)
            thumbnail = await Gthumb02(bot, update, duration, file_location)
            await bot.send_video_note(chat_id=update.message.chat.id,
            video_note=file_location,
            duration=duration,
            length=width,
            thumb=thumb_image_path,
            reply_to_message_id=update.message.reply_to_message.message_id,
            progress=progress_for_pyrogram,
            progress_args=(Translation.UPLOAD_START, update.message, start_time))
        elif tg_send_type == "video":
            width, height, duration = await Mdata01(file_location)
            thumbnail = await Gthumb02(bot, update, duration, file_location)
            await bot.send_video(chat_id=update.message.chat.id,
            video=file_location,
            caption=description,
            parse_mode="HTML",
            duration=duration,
            width=width,
            height=height,
            thumb=thumbnail,
            supports_streaming=True,
            reply_to_message_id=update.message.reply_to_message.message_id,
            progress=progress_for_pyrogram,
            progress_args=(Translation.UPLOAD_START,
            update.message, start_time) )
        else:
            thumbnail = await Gthumb01(bot, update)
            await bot.send_document(chat_id=update.message.chat.id,
            document=file_location,
            thumb=thumbnail,
            caption=description,
            parse_mode="HTML",
            reply_to_message_id=update.message.reply_to_message.message_id,
            progress=progress_for_pyrogram,
            progress_args=(Translation.UPLOAD_START, update.message, start_time))

        asyncio.create_task(clendir(file_location))
        asyncio.create_task(clendir(thumbnail))
        await bot.edit_message_text(
        text="Uploaded sucessfully ✓\n\nJOIN : @SPACE_X_BOTS",
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
        disable_web_page_preview=True)
    except Exception as e:
        asyncio.create_task(clendir(download_directory))
        await bot.edit_message_text(text=Translation.ERROR.format(e),
        chat_id=update.message.chat.id, message_id=update.message.message_id)

#=================================

async def clendir(directory):

    try:
        os.remove(directory)
    except:
        pass
    try:
        shutil.rmtree(directory)
    except:
        pass

#=================================
