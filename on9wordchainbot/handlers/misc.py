from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from on9wordchainbot import dp, bot
from on9wordchainbot.utils import get_user, add_user, get_group, add_group

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_TEXT = """
Hi👋 {user}!

I'm {bot} – your fun companion from 𝑽𝒆𝒍𝒐𝒄𝒊𝒕𝒚 𝐗 𝗪𝗼𝗿𝗱 𝗖𝗵𝗮𝗶𝗻 🎮

Play exciting word chain games with your friends in Telegram groups.
➕ Add me to a group and type `/start` to begin the fun!
"""

PHOTO_URL = "https://graph.org/file/046efb7c1411d26be3145-a751e2c61b39111484.jpg"

@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username or ""
    first_name = message.from_user.first_name or "User"

    # Save user if not already saved
    if not await get_user(user_id):
        await add_user(user_id, user_name, first_name)

    # Group chat handling
    if message.chat.type in ["group", "supergroup"]:
        if not await get_group(message.chat.id):
            await add_group(message.chat.id, message.chat.title)

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=PHOTO_URL,
            caption=START_TEXT.format(
                user=message.from_user.get_mention(),
                bot=(await bot.get_me()).first_name
            )
        )
    else:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=PHOTO_URL,
            caption=START_TEXT.format(
                user=message.from_user.get_mention(),
                bot=(await bot.get_me()).first_name
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{(await bot.get_me()).username}?startgroup=true")],
                [
                    InlineKeyboardButton("👥 Group", url="https://t.me/+5vPKU47S6HNiNjY1"),
                    InlineKeyboardButton("🔄 Updates", url="https://t.me/Who_Cares_qt")
                ],
                [InlineKeyboardButton("ɢx ᴅᴀʀᴋ ʙᴏᴛs [🇮🇳]", url="https://t.me/dark_x_knight_musiczz_support")]
            ])
        )