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
						InlineKeyboardButton("👥 𝐇𝐞𝐥𝐩", callback_data="help"),
						InlineKeyboardButton("🌐 𝐒𝐨𝐮𝐫𝐜𝐞 𝐂𝐨𝐝𝐞", url="https://t.me/MoviesFlixers_DL")
					],
					[
						InlineKeyboardButton("🏠 𝐇𝐨𝐦𝐞", callback_data="gotohome") 
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
						InlineKeyboardButton("𝐒𝐨𝐮𝐫𝐜𝐞 𝐂𝐨𝐝𝐞𝐬 𝐨𝐟 𝐁𝐨𝐭 ", url="https://t.me/Moviesflixers_DL")
					],
					[
						InlineKeyboardButton("👥 𝐀𝐛𝐨𝐮𝐭 ", callback_data="aboutbot"),
						InlineKeyboardButton("🏠 𝐇𝐨𝐦𝐞", callback_data="gotohome")
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
						InlineKeyboardButton("🛑 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 🛑", url="https://t.me/TeleRoid14"),
						InlineKeyboardButton("⭕ 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ⭕", url="https://t.me/TeleRoidGroup")
					],
					[
						InlineKeyboardButton("👥 𝐀𝐛𝐨𝐮𝐭 ", callback_data="aboutbot"),
						InlineKeyboardButton("🗣️ 𝐇𝐞𝐥𝐩 ", callback_data="help")
					], 
                                        [
						InlineKeyboardButton("🌐 𝐆𝐢𝐭𝐡𝐮𝐛 ", url="https://GitHub.com/PredatorHackerzZ"),
						InlineKeyboardButton("📢 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲", url="https://t.me/MoviesFlixers_DL")
	            ]
                ]
            )
        )

@Clinton.on_callback_query()
async def button(bot, update):
 
      if  'close'  in update.data:
                await update.message.delete()
