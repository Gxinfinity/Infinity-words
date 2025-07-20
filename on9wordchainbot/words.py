import asyncio
import logging
from typing import List

from dawg_python import DAWG  # 👈 Yeh line badli hai

from .constants import WORDLIST_SOURCE

logger = logging.getLogger(__name__)


class Words:
    dawg: DAWG
    count: int

    @staticmethod
    async def update() -> None:
        logger.info("Retrieving words")

        async def get_words_from_source() -> List[str]:
            from . import session
            async with session.get(WORDLIST_SOURCE) as resp:
                return (await resp.text()).splitlines()

        async def get_words_from_db() -> List[str]:
            from . import pool
            async with pool.acquire() as conn:
                res = await conn.fetch("SELECT word FROM wordlist WHERE accepted;")
                return [row[0] for row in res]

        source_task = asyncio.create_task(get_words_from_source())
        db_task = asyncio.create_task(get_words_from_db())
        wordlist = await source_task + await db_task

        logger.info("Processing words")
        wordlist = [w.lower() for w in wordlist if w.isalpha()]

        Words.dawg = DAWG()  # 👈 Yeh bhi badla
        Words.dawg.build(wordlist)  # 👈 Ab ye error nahi dega
        Words.count = len(Words.dawg.keys())

        logger.info("DAWG updated")