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
from helper_funcs.forcesub import ForceSub
from pyrogram import filters
from database.adduser import AddUser
from pyrogram import Client as Clinton
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


@Clinton.on_message(filters.private & filters.command(["help"]))
async def help_user(bot, update):
    # logger.info(update)
    await AddUser(bot, update)
    forcesub = await ForceSub(bot, update)
    if forcesub == 400:
        return
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="⭕️ Join Updates Channel ⭕️", url="https://t.me/TeleRoidGroup")]]),
   )


@Clinton.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    # logger.info(update)
    await AddUser(bot, update)
    forcesub = await ForceSub(bot, update)
    if forcesub == 400:
        return
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.mention),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id,
        reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text="💰 Donate 💰", url="https://PayPal.me/AbhishekKumarIN47") ], 
                                             [ InlineKeyboardButton(text="⭕ Support Group ⭕", url="https://t.me/TeleRoid14"),
                                               InlineKeyboardButton(text="⭕️ Updates Channel ⭕️", url="https://t.me/TeleRoidGroup") ],
                                             [ InlineKeyboardButton(text="♻ Help ", callback_data="help"),                                                
                                               InlineKeyboardButton(text="👥 About ", callback_data="aboutbot") ], 
                                             [ InlineKeyboardButton(text="🔐 Close🔐", callback_data="close") ] ] ) )

@Clinton.on_message(filters.private & filters.command("about") )
async def about(bot, update):
    # logger.info(update)
    await AddUser(bot, update)
    forcesub = await ForceSub(bot, update)
    if forcesub == 400:
        return
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id,
        reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text="🚸 Powered By", url="https://t.me/TeleRoidGroup") ],
                                             [ InlineKeyboardButton(text="⭕ Support Group ⭕", url="https://t.me/TeleRoid14"),
                                               InlineKeyboardButton(text="💢 Source Code", url="https://github.com/PredatorHackerzZ") ] ] ) )

