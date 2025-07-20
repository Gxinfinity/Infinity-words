from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher

from ..utils import get_user, add_user, get_group, add_group

START_TEXT = """
Hi👋 {name}!

I'm your fun companion from 𝑽𝒆𝒍𝒐𝒄𝒊𝒕𝒚 𝐗 𝗪𝗼𝗿𝗱 𝗖𝗵𝗮𝗶𝗻 🎮

Play exciting word chain games with your friends in Telegram groups.
➕ Add me to a group and type `/start` to begin the fun!
"""

PHOTO_URL = "https://graph.org/file/046efb7c1411d26be3145-a751e2c61b39111484.jpg"

async def start_cmd(message: types.Message):
    user = message.from_user

    # Save user if not already saved
    if not await get_user(user.id):
        await add_user(user.id, user.username or "", user.first_name or "User")

    # Group chat
    if message.chat.type in ["group", "supergroup"]:
        if not await get_group(message.chat.id):
            await add_group(message.chat.id, message.chat.title)

        await message.reply_photo(
            photo=PHOTO_URL,
            caption=START_TEXT.format(name=user.first_name),
        )
    else:
        # Private chat
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{(await message.bot.get_me()).username}?startgroup=true"),
            InlineKeyboardButton("👥 Group", url="https://t.me/+5vPKU47S6HNiNjY1"),
            InlineKeyboardButton("🔄 Updates", url="https://t.me/Who_Cares_qt"),
        )
        keyboard.add(
            InlineKeyboardButton("ɢx ᴅᴀʀᴋ ʙᴏᴛs [🇮🇳]", url="https://t.me/dark_x_knight_musiczz_support")
        )

        await message.answer_photo(
            photo=PHOTO_URL,
            caption=START_TEXT.format(name=user.first_name),
            reply_markup=keyboard
        )

def register_handlers_misc(dp: Dispatcher):
    dp.register_message_handler(start_cmd, Command("start", "help"))