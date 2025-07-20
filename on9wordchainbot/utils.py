import random
from string import ascii_lowercase
from typing import Optional, List, Set

from aiogram import types
from . import bot
from .constants import ADMIN_GROUP_ID
from .words import Words

def is_word(s: str) -> bool:
    return all(c in ascii_lowercase for c in s)

def check_word_existence(word: str) -> bool:
    return word in Words.dawg

def filter_words(
    min_len: int = 1,
    prefix: Optional[str] = None,
    required_letter: Optional[str] = None,
    banned_letters: Optional[List[str]] = None,
    exclude_words: Optional[Set[str]] = None
) -> List[str]:
    words = Words.dawg.keys(prefix) if prefix else Words.dawg.keys()
    if min_len > 1:
        words = [w for w in words if len(w) >= min_len]
    if required_letter:
        words = [w for w in words if required_letter in w]
    if banned_letters:
        words = [w for w in words if all(i not in w for i in banned_letters)]
    if exclude_words:
        words = [w for w in words if w not in exclude_words]
    return words

def get_random_word(
    min_len: int = 1,
    prefix: Optional[str] = None,
    required_letter: Optional[str] = None,
    banned_letters: Optional[List[str]] = None,
    exclude_words: Optional[Set[str]] = None
) -> Optional[str]:
    words = filter_words(min_len, prefix, required_letter, banned_letters, exclude_words)
    return random.choice(words) if words else None

def inline_keyboard_from_button(button: types.InlineKeyboardButton) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[button]])

ADD_TO_GROUP_KEYBOARD = inline_keyboard_from_button(
    types.InlineKeyboardButton("➕ Add Me To Group", url="https://t.me/on9wordchainbot?startgroup=true")
)