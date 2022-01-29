
# (c) @AbirHasan2005 | Modifieded By : @DC4_WARRIOR


from pyrogram import Client as Clinton
from pyrogram import filters
from config import Config
from database.access import clinton
from plugins.buttons import *
@Clinton.on_message(filters.private & filters.command('total'))
async def sts(c, m):
    if m.from_user.id != Config.OWNER_ID:
        return 
    total_users = await clinton.total_users_count()
    await m.reply_text(text=f"Total user(s) {total_users}", quote=True)


@Clinton.on_message(filters.private & filters.command("search"))
async def serc(bot, update):

      await bot.send_message(chat_id=update.chat.id, text="🔍 TORRENT SEARCH", 
      parse_mode="html", reply_markup=Button.BUTTONS01)
