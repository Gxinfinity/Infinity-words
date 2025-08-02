from aiogram import types
from aiogram.types import Message
from typing import Optional, Any

from .constants import ADMIN_GROUP_ID
from .filters import get_current_username
from .models import Game, User
from .words import get_next_word
from .__main__ import bot

def clean_word(word: str) -> str:
    return word.strip().lower()

def is_valid_word(word: str, prev_word: str) -> bool:
    return word.startswith(prev_word[-1]) and word != prev_word

def is_valid_answer(answer: str, prev_word: str) -> bool:
    return is_valid_word(answer, prev_word) and get_next_word(answer) is not None

async def send_admin_group(*args: Any, **kwargs: Any) -> Optional[types.Message]:
    try:
        return await bot.send_message(ADMIN_GROUP_ID, *args, **kwargs)
    except Exception as e:
        print(f"❌ Failed to send message to admin group (ID: {ADMIN_GROUP_ID}): {e}")
        return None

def format_word(word: str) -> str:
    return f"**{word}**"

def format_user(user: types.User) -> str:
    name = get_current_username(user)
    return f"[{name}](tg://user?id={user.id})"

def get_user_score(user: types.User, game: Game) -> int:
    for player in game.players:
        if player.user_id == user.id:
            return player.score
    return 0

def get_user(game: Game, telegram_user: types.User) -> Optional[User]:
    for player in game.players:
        if player.user_id == telegram_user.id:
            return player
    return None

def get_last_word(game: Game) -> Optional[str]:
    if game.words:
        return game.words[-1]
    return None