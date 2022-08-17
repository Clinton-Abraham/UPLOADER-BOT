#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Modified By > @Clinton_Abraham

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

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
    cb_data = update.data
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("|")
    save_ytdl_json_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except (FileNotFoundError) as e:
        await update.message.delete(True)
        return False
    youtube_dl_url = update.message.reply_to_message.text
    custom_file_name = str(response_json.get("title"))[:50] + "_" + youtube_dl_format + "." + youtube_dl_ext
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
    await bot.edit_message_text(
    text=Translation.DOWNLOAD_START,
    chat_id=update.message.chat.id,
    message_id=update.message.message_id)
    description = Translation.CUSTOM_CAPTION_UL_FILE
    if "fulltitle" in response_json:
        description = response_json["fulltitle"][0:1021]
        # escape Markdown and special characters
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    if '/' in custom_file_name:
        file_mimx = custom_file_name
        file_maix = file_mimx.split('/')
        file_name = ' '.join(file_maix)
    else:
        file_name = custom_file_name
    download_directory = tmp_directory_for_each_user + "/" + str(file_name)
    command_to_exec = []
    if tg_send_type == "audio":
        command_to_exec = ["yt-dlp", "-c",
             "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
             "--prefer-ffmpeg", "--extract-audio",
             "--audio-format", youtube_dl_ext,
             "--audio-quality", youtube_dl_format,
             youtube_dl_url, "-o", download_directory]
    else:
        minus_f_format = youtube_dl_format
        if "youtu" in youtube_dl_url:
            minus_f_format = youtube_dl_format + "+bestaudio"
        command_to_exec = ["yt-dlp", "-c",
            "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            "--embed-subs", "-f", minus_f_format,
            "--hls-prefer-ffmpeg", youtube_dl_url,
            "-o", download_directory]

    if Config.HTTP_PROXY != "":
        command_to_exec.append("--proxy")
        command_to_exec.append(Config.HTTP_PROXY)
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    command_to_exec.append("--no-warnings")
    command_to_exec.append("--quiet")

    start = datetime.now()
    process = await asyncio.create_subprocess_exec(*command_to_exec,
    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,)

    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()

    ad_string_to_replace = "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output."
    if e_response and ad_string_to_replace in e_response:
        error_message = e_response.replace(ad_string_to_replace, "")
        await bot.edit_message_text(
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
        text=error_message)
        return False
    if t_response:
        asyncio.create_task(clendir(save_ytdl_json_path))
        try:
            file_size = os.stat(download_directory).st_size
        except FileNotFoundError:
            try:
                download_directory = os.path.splitext(download_directory)[0] + "." + "mkv"
                file_size = os.stat(download_directory).st_size
            except Exception:
                await update.message.edit(text="File Not found 🤒")
                asyncio.create_task(clendir(tmp_directory_for_each_user))
                return
        if file_size > Config.TG_MAX_FILE_SIZE:
            await bot.edit_message_text(
            chat_id=update.message.chat.id,
            text=Translation.RCHD_TG_API_LIMIT.format(time_taken_for_download, humanbytes(file_size)),
            message_id=update.message.message_id)
        else:
            await bot.edit_message_text(
            text=Translation.UPLOAD_START,
            chat_id=update.message.chat.id,
            message_id=update.message.message_id)
            try:
                start_time = time.time()
                if tg_send_type == "audio":
                    duration = await Mdata03(download_directory)
                    thumbnail = await Gthumb01(bot, update)
                    await bot.send_audio(
                    chat_id=update.message.chat.id,
                    audio=download_directory,
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
                    document=download_directory,
                    thumb=thumbnail,
                    caption=description,
                    parse_mode="HTML",
                    reply_to_message_id=update.message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time))
                elif tg_send_type == "vm":
                    width, duration = await Mdata02(download_directory)
                    thumbnail = await Gthumb02(bot, update, duration, download_directory)
                    await bot.send_video_note(chat_id=update.message.chat.id,
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thumb=thumb_image_path,
                    reply_to_message_id=update.message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time))
                elif tg_send_type == "video":
                    width, height, duration = await Mdata01(download_directory)
                    thumbnail = await Gthumb02(bot, update, duration, download_directory)
                    await bot.send_video(chat_id=update.message.chat.id,
                    video=download_directory,
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

                asyncio.create_task(clendir(download_directory))
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

#=================================
