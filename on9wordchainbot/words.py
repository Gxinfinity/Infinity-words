import asyncio
import logging
from typing import List, Set

from .constants import WORDLIST_SOURCE

logger = logging.getLogger(__name__)


class Words:
    dawg: Set[str] = set()
    count: int = 0

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

        source_words, db_words = await asyncio.gather(
            get_words_from_source(), get_words_from_db()
        )

        wordlist = [w.lower() for w in source_words + db_words if w.isalpha()]

        Words.dawg = set(wordlist)
        Words.count = len(Words.dawg)

        logger.info(f"Word set updated