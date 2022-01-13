import os

class Config(object):
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("5055897853:AAH38dJbwwImUDhFJW5SZUQFOWrLNyOfGWQ", "")
    # The Telegram API things
    APP_ID = int(os.environ.get("7275264", 12345))
    API_HASH = os.environ.get("6a5b202320d2e67f19fb43fb294f17a3")
    # Get these values from my.telegram.org
    # Banned Unwanted Members..
    BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())
    # the download location, where the HTTP Server runs
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    # Update channel for Force Subscribe
    UPDATE_CHANNEL = os.environ.get("@kashir_bots", "")
    # Telegram maximum file upload size
    MAX_FILE_SIZE = 50000000
    TG_MAX_FILE_SIZE = 2097152000
    FREE_USER_MAX_FILE_SIZE = 50000000
    # chunk size that should be used with requests
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    # default thumbnail to be used in the videos
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "")
    # proxy for accessing youtube-dl in GeoRestricted Areas
    # Get your own proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # set timeout for subprocess
    PROCESS_MAX_TIMEOUT = 3600
    # watermark file
    DEF_WATER_MARK_FILE = ""
    # your telegram id
    OWNER_ID = int(os.environ.get("1983594747", ""))
    # database session name, example: xurluploader
    SESSION_NAME = os.environ.get("SESSION_NAME", "")
    # database uri (mongodb)
    DATABASE_URL = os.environ.get("mongodb+srv://paidchu:paidchu@cluster0.s6o4g.mongodb.net/cluster0?retryWrites=true&w=majority", "")
