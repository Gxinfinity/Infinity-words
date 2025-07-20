from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher

from on9wordchainbot import dp  # ya jahan se dp import hota ho
from ..utils import get_user, add_user, get_group, add_group


START_TEXT = """
Hi {user}!

I'm {bot} – your fun companion from 𝑽𝒆𝒍𝒐𝒄𝒊𝒕𝒚 𝐗 𝗪𝗼𝗿𝗱 𝗖𝗵𝗮𝗶𝗻 🎮

Play exciting word chain games with your friends in Telegram groups.
➕ Add me to a group and type `/start` to begin the fun!
"""


@dp.message_handler(CommandStart() | CommandHelp())
async def start(message: types.Message):
    user = message.from_user
    user_id = user.id
    user_name = user.username or ""
    first_name = user.first_name or "User"

    # Save user if not already saved
    if not get_user(user_id):
        await add_user(user_id, user_name, first_name)

    # Group chat
    if message.chat.type in ["group", "supergroup"]:
        if not get_group(message.chat.id):
            await add_group(message.chat.id, message.chat.title)

        await message.reply_photo(
            photo="https://graph.org/file/046efb7c1411d26be3145-a751e2c61b39111484.jpg",
            caption=START_TEXT.format(
                user=message.from_user.get_mention(as_html=True),
                bot=message.bot.first_name
            ),
            parse_mode="HTML"
        )
    else:
        # Private chat
        await message.reply_photo(
            photo="https://graph.org/file/046efb7c1411d26be3145-a751e2c61b39111484.jpg",
            caption=START_TEXT.format(
                user=message.from_user.get_mention(as_html=True),
                bot=message.bot.first_name
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{message.bot.username}?startgroup=true")],
                [