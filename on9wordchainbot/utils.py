import logging
from pyrogram.types import InlineKeyboardMarkup

logger = logging.getLogger(__name__)


# ✅ Convert custom buttons to InlineKeyboardMarkup
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


# ✅ Check if user is VIP
def has_star(user_id: int):
    from config import VIP_USERS
    return user_id in VIP_USERS


# ✅ Logging to admin group
async def send_admin_group(client, text):
    from config import ADMIN_GROUP_ID
    try:
        await client.send_message(chat_id=ADMIN_GROUP_ID, text=text)
    except Exception as e:
        logger.error(f"Failed to send admin log: {e}")