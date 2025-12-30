import asyncio
import logging
from datetime import datetime
from typing import Dict, TYPE_CHECKING

import aiohttp
import asyncpg
from aiogram import Bot, Dispatcher, types

from .constants import DB_URI, ON9BOT_TOKEN, TOKEN
from .filters import filters

if TYPE_CHECKING:
    from .models import ClassicGame

try:
    import coloredlogs
except ImportError:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
else:
    coloredlogs.install(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

logger = logging.getLogger(__name__)

try:
    import uvloop
except ImportError:
    logger.info(r"uvloop unavailable ¯\_(ツ)_/¯")
else:
    uvloop.install()

loop = asyncio.get_event_loop()

# ✅ SIMPLE & CORRECT FOR aiogram 2.25.1
bot = Bot(
    TOKEN,
    parse_mode=types.ParseMode.MARKDOWN,
    disable_web_page_preview=True,
)

on9bot = Bot(ON9BOT_TOKEN)

dp = Dispatcher(bot)

# Keep session only for your own HTTP / shutdown logic
session = aiohttp.ClientSession()

pool: asyncpg.pool.Pool


class GlobalState:
    build_time = datetime.now().replace(microsecond=0)
    maint_mode = False

    games: Dict[int, "ClassicGame"] = {}
    games_lock: asyncio.Lock = asyncio.Lock()


async def init() -> None:
    global pool
    logger.info("Connecting to database")
    pool = await asyncpg.create_pool(DB_URI, loop=loop)


loop.run_until_complete(init())

for f in filters:
    dp.filters_factory.bind(f)

from .handlers import *  # noqa