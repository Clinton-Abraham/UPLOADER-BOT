# (c) @AbirHasan2005 | @PredatorHackerzZ

import asyncio
from sample_config import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

async def ForceSub(bot: Client, cmd: Message):
    try:
        user = await bot.get_chat_member(chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATE_CHANNEL.startswith("-100") else Config.UPDATE_CHANNEL), user_id=cmd.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="Sorry Son, You are Banned to use me. Contact my [Support Group](https://t.me/TeleRoid14).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!\n\nAnd Still If Bot AskS For Joining Updates Channel then Join @MoviesFlixers_DL.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url="https://t.me/TeleRoidGroup")
                    ]
                ]
            ),
            parse_mode="markdown"
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="Something went Wrong. Contact my [Support Group](https://t.me/TeleRoid14).\n\n**@TheTeleRoid**",
            parse_mode="markdown",
            disable_web_page_preview=True
        )
        return 400
    return 200
