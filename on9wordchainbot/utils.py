import logging
from pyrogram.types import InlineKeyboardMarkup
from .db import db  # Make sure this exists

logger = logging.getLogger(__name__)


# ✅ Send admin group logging
async def send_admin_group(client, text):
    from config import ADMIN_GROUP_ID
    try:
        await client.send_message(chat_id=ADMIN_GROUP_ID, text=text)
    except Exception as e:
        logger.error(f"Failed to send admin log: {e}")


# ✅ Convert custom button format to InlineKeyboardMarkup
def inline_keyboard_from_button(buttons):
    if not buttons:
        return None
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for btn in row:
            keyboard_row.append(btn)
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(keyboard)


# ✅ Check if a user has a star (VIP)
def has_star(user_id: int):
    from config import VIP_USERS
    return user_id in VIP_USERS


# ✅ DATABASE FUNCTIONS — required by handlers
async def get_user(user_id: int):
    query = "SELECT * FROM users WHERE user_id = $1"
    return await db.fetchrow(query, user_id)


async def add_user(user_id: int, username: str, full_name: str):
    query = """
        INSERT INTO users (user_id, username, full_name)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id) DO NOTHING
    """
    await db.execute(query, user_id, username, full_name)


async def get_group(chat_id: int):
    query = "SELECT * FROM groups WHERE group_id = $1"
    return await db.fetchrow(query, chat_id)


async def add_group(chat_id: int, name: str):
    query = """
        INSERT INTO groups (group_id, name)
        VALUES ($1, $2)
        ON CONFLICT (group_id) DO NOTHING
    """
    await db.execute(query, chat_id, name)