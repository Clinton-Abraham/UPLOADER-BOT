
import aiohttp
from config import Config
from requests.utils import requote_uri

API_1337x = "https://api.abirhasan.wtf/1337x?query={}&limit={}"
API_YTS = "https://api.abirhasan.wtf/yts?query={}&limit={}"
API_PIRATEBAY = "https://api.abirhasan.wtf/piratebay?query={}&limit={}"
API_ANIME = "https://api.abirhasan.wtf/anime?query={}&limit={}"


async def Search1337x(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(requote_uri(API_1337x.format(query, Config.MAX_RESULTS))) as res:
            return (await res.json())["results"] if ((await res.json()).get("results", None) is not None) else []


async def SearchYTS(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(requote_uri(API_YTS.format(query, Config.MAX_RESULTS))) as res:
            return (await res.json())["results"] if ((await res.json()).get("results", None) is not None) else []


async def SearchPirateBay(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(requote_uri(API_PIRATEBAY.format(query, Config.MAX_RESULTS))) as res:
            return (await res.json())["results"] if ((await res.json()).get("results", None) is not None) else []


async def SearchAnime(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(requote_uri(API_ANIME.format(query, Config.MAX_RESULTS))) as res:
            return (await res.json())["results"] if ((await res.json()).get("results", None) is not None) else []

