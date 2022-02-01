#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | Modified By > @DC4_WARRIOR


from pyrogram import Client as Clinton
from plugins.youtube_dl_button import youtube_dl_call_back
from plugins.dl_button import ddl_call_back

from translation import Translation

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery



@Clinton.on_callback_query()
async def button(bot, update):

    cb_data = update.data
    if "|" in cb_data:
        await youtube_dl_call_back(bot, update)
    elif "=" in cb_data:
        await ddl_call_back(bot, update)
    elif "aboutbot" in cb_data:
        await update.message.edit(
            text=Translation.ABOUT_TEXT,
            parse_mode="html",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
					[
						InlineKeyboardButton("🆘 Help", callback_data="help"),
						InlineKeyboardButton("🐱 SourceCode", url="https://github.com/PredatorHackerzZ/UPLOADER-BOT")
					],
					[
						InlineKeyboardButton("🏡 Home", callback_data="gotohome"),
						InlineKeyboardButton("🔐 Close", callback_data="close")
					]
	        ]
            )
        )

    elif "help" in cb_data:
        await update.message.edit(
            text=Translation.HELP_USER,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                                        [
						InlineKeyboardButton("👥 About ", callback_data="aboutbot"),
						InlineKeyboardButton("🐱 SourceCode", url="https://github.com/PredatorHackerzZ/UPLOADER-BOT")
					],
					[
						InlineKeyboardButton("🏡 Home", callback_data="gotohome"),
						InlineKeyboardButton("🔐 Close ", callback_data="close")
					]
                ]
            )
        )

    elif "gotohome" in cb_data:
        await update.message.edit(
            text=Translation.START_TEXT.format(update.from_user.mention),
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
						InlineKeyboardButton("⭕ Channel ⭕", url="https://t.me/TeleRoidGroup"),
						InlineKeyboardButton("😇 Support", url="https://t.me/TeleRoid14")
					],
					[
						InlineKeyboardButton("👥 About", callback_data="aboutbot"),
						InlineKeyboardButton("🆘 Help", callback_data="help")
					],
                                        [
						InlineKeyboardButton("😺 GitHub", url="https://GitHub.com/PredatorHackerzZ"),
						InlineKeyboardButton("💸 Donate", url="https://paypal.me/AbhishekKumarIN47")
	                                ],
                                        [
						InlineKeyboardButton("🔐 Close", callback_data="close")
	            ]
                ]
            )
        )

@Clinton.on_callback_query()
async def button(bot, update):
 
      if  'close'  in update.data:
                await update.message.delete()
