#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import sqlite3

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

from pyrogram import filters
from database.adduser import AddUser
from pyrogram import Client as Clinton
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Clinton.on_message(filters.private & filters.command(["help"]))
async def help_user(bot, update):
    # logger.info(update)
    await AddUser(bot, update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="⭕️ 𝐉𝐎𝐈𝐍 𝐎𝐔𝐑 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ⭕️", url="https://t.me/TeleRoidGroup")]]),
   )


@Clinton.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    # logger.info(update)
    await AddUser(bot, update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.mention),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id,
        reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text="⭕️ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ⭕️", url="https://t.me/TeleRoidGroup") ], 
                                             [ InlineKeyboardButton(text="🛑 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 🛑", url="https://t.me/TeleRoid14"),
                                               InlineKeyboardButton(text=" 𝐀𝐛𝐨𝐮𝐭 𝐌𝐞 ", url="https://t.me/TheTeleRoid") ],
                                             [ InlineKeyboardButton(text="♻ 𝐇𝐞𝐥𝐩 ", callback_data="HELP_USER"),                                                
                                               InlineKeyboardButton(text="👥 𝐀𝐛𝐨𝐮𝐭", callback_data="ABOUT_TEXT") ] ] ) )
