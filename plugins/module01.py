
"""

async def inlineX1(bot, update):

          answers = []
          search_ts = update.query
          query = search_ts.split(" ", 1)[-1]
          torrentList = await SearchYTS(query)
          if not torrentList:
              answers.append(InlineQueryResultArticle(title="No Torrents Found in ThePirateBay!",
              description=f"Can't find torrents for {query} in ThePirateBay !!",
              input_message_content=InputTextMessageContent(
              message_text=f"No Torrents Found For `{query}` in ThePirateBay !!", parse_mode="Markdown"),
              reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!pb ") ] ] ) ) )
          else:
              for i in range(len(torrentList)):
                  dl_links = "- " + "\n\n- ".join(torrentList[i]['Downloads'] )
                  answers.append(InlineQueryResultArticle(title=f"{torrentList[i]['Name']}",
                  description=f"Language: {torrentList[i]['Language']}\nLikes: {torrentList[i]['Likes']}, Rating: {torrentList[i]['Rating']}",
                  input_message_content=InputTextMessageContent(
                  message_text=f"**Genre:** `{torrentList[i]['Genre']}`\n"
                               f"**Name:** `{torrentList[i]['Name']}`\n"
                               f"**Language:** `{torrentList[i]['Language']}`\n"
                               f"**Likes:** `{torrentList[i]['Likes']}`\n"
                               f"**Rating:** `{torrentList[i]['Rating']}`\n"
                               f"**Duration:** `{torrentList[i]['Runtime']}`\n"
                               f"**Released on {torrentList[i]['ReleaseDate']}**\n\n"
                               f"**Torrent Download Links:**\n{dl_links}",
                               parse_mode="Markdown", disable_web_page_preview=True),
                  reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!yts ") ] ] ),
                  thumb_url=torrentList[i]["Poster"] ) )
          try:
              await update.answer(results=answers, cache_time=0)
          except QueryIdInvalid:
              await asyncio.sleep(5)
          try:
              await update.answer(results=answers, cache_time=0,
              switch_pm_text="Error: Search timed out!",
              switch_pm_parameter="start",)
          except QueryIdInvalid:
              pass


async def inlineX2(bot, update):


          answers = []
          search_ts = update.query
          query = search_ts.split(" ", 1)[-1]
          torrentList = await SearchAnime(query)
          if not torrentList:
              answers.append(InlineQueryResultArticle(title="No Torrents Found!",
              description=f"Can't find YTS torrents for {query} !!",
              input_message_content=InputTextMessageContent(
              message_text=f"No YTS Torrents Found For `{query}`", parse_mode="Markdown"),
              reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!yts ") ] ] ) ) )
          else:
              for i in range(len(torrentList)):
                  answers.append(InlineQueryResultArticle(title=f"{torrentList[i]['Name']}",
                  description=f"Seeders: {torrentList[i]['Seeders']}, Leechers: {torrentList[i]['Leechers']}\nSize: {torrentList[i]['Size']}",
                  input_message_content=InputTextMessageContent(
                  message_text=f"**Category:** `{torrentList[i]['Category']}`\n"
                               f"**Name:** `{torrentList[i]['Seeders']}`\n"
                               f"**Size:** `{torrentList[i]['Size']}`\n"
                               f"**Seeders:** `{torrentList[i]['Seeders']}`\n"
                               f"**Leechers:** `{torrentList[i]['Leechers']}`\n"
                               f"**Uploader:** `{torrentList[i]['Uploader']}`\n"
                               f"**Uploaded on {torrentList[i]['Date']}**\n\n"
                               f"**Magnet:**\n`{torrentList[i]['Magnet']}`", parse_mode="Markdown"),
                      reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!pb ") ] ] ) ) )

          try:
              await update.answer(results=answers, cache_time=0)
          except QueryIdInvalid:
              await asyncio.sleep(5)
          try:
              await update.answer(results=answers, cache_time=0,
              switch_pm_text="Error: Search timed out!",
              switch_pm_parameter="start",)
          except QueryIdInvalid:
              pass


async def inlineX3(bot, update):

          answers = []
          search_ts = update.query
          query = search_ts.split(" ", 1)[-1]
          torrentList = await Search1337x(query)
          if not torrentList:
              answers.append(InlineQueryResultArticle(title="No Anime Torrents Found!",
              description=f"Can't find Anime torrents for {query} !!",
              input_message_content=InputTextMessageContent(message_text=f"No Anime Torrents Found For `{query}`", parse_mode="Markdown"),
              reply_markup=InlineKeyboardMarkup( [ [InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!a ") ] ] ) ) )
          else:
              for i in range(len(torrentList)):
                  answers.append(InlineQueryResultArticle(title=f"{torrentList[i]['Name']}",
                  description=f"Seeders: {torrentList[i]['Seeder']}, Leechers: {torrentList[i]['Leecher']}\nSize: {torrentList[i]['Size']}",
                  input_message_content=InputTextMessageContent(
                  message_text=f"**Category:** `{torrentList[i]['Category']}`\n"
                               f"**Name:** `{torrentList[i]['Name']}`\n"
                               f"**Seeders:** `{torrentList[i]['Seeder']}`\n"
                               f"**Leechers:** `{torrentList[i]['Leecher']}`\n"
                               f"**Size:** `{torrentList[i]['Size']}`\n"
                               f"**Upload Date:** `{torrentList[i]['Date']}`\n\n"
                               f"**Magnet:** \n`{torrentList[i]['Magnet']}`", parse_mode="Markdown"),
                  reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!a ") ] ] ) ) )

          try:
              await update.answer(results=answers, cache_time=0)
          except QueryIdInvalid:
              await asyncio.sleep(5)
          try:
              await update.answer(results=answers, cache_time=0,
              switch_pm_text="Error: Search timed out!",
              switch_pm_parameter="start",)
          except QueryIdInvalid:
              pass


async def inlineX4(bot, update):

          answers = []
          search_ts = update.query
          query = search_ts.split(" ", 1)[-1]
          torrentList = await SearchPirateBay(query)
          if not torrentList:
              answers.append(InlineQueryResultArticle(title="No Anime Torrents Found!",
              description=f"Can't find Anime torrents for {query} !!",
              input_message_content=InputTextMessageContent(message_text=f"No Anime Torrents Found For `{query}`", parse_mode="Markdown"),
              reply_markup=InlineKeyboardMarkup( [ [InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!a ") ] ] ) ) )
          else:
              for i in range(len(torrentList)):
                  answers.append(InlineQueryResultArticle(title=f"{torrentList[i]['Name']}",
                  description=f"Seeders: {torrentList[i]['Seeder']}, Leechers: {torrentList[i]['Leecher']}\nSize: {torrentList[i]['Size']}",
                  input_message_content=InputTextMessageContent(
                  message_text=f"**Category:** `{torrentList[i]['Category']}`\n"
                               f"**Name:** `{torrentList[i]['Name']}`\n"
                               f"**Seeders:** `{torrentList[i]['Seeder']}`\n"
                               f"**Leechers:** `{torrentList[i]['Leecher']}`\n"
                               f"**Size:** `{torrentList[i]['Size']}`\n"
                               f"**Upload Date:** `{torrentList[i]['Date']}`\n\n"
                               f"**Magnet:** \n`{torrentList[i]['Magnet']}`", parse_mode="Markdown"),
                  reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!a ") ] ] ) ) )

          try:
              await update.answer(results=answers, cache_time=0)
          except QueryIdInvalid:
              await asyncio.sleep(5)
          try:
              await update.answer(results=answers, cache_time=0,
              switch_pm_text="Error: Search timed out!",
              switch_pm_parameter="start",)
          except QueryIdInvalid:
              pass


"""
