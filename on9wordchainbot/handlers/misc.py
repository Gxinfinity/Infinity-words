from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from on9wordchainbot import dp
from on9wordchainbot.utils import get_user, add_user, get_group, add_group


START_TEXT = """
Hi {user}!

I'm {bot} – your fun companion from 𝑽𝒆𝒍𝒐𝒄𝒊𝒕𝒚 𝐗 𝗪𝗼𝗿𝗱 𝗖𝗵𝗮𝗶𝗻 🎮

Play exciting word chain games with your friends in Telegram groups.
➕ Add me to a group and type `/start` to begin the fun!
"""

PHOTO_URL = "https://graph.org/file/046efb7c1411d26be3145-a751e2c61b39111484.jpg"


@dp.message_handler(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    user = message.from_user
    chat = message.chat

    # Save user if not already saved
    if not await get_user(user.id):
        await add_user(user.id, user.username or "", user.first_name or "User")

    # If group chat
    if chat.type in ("group", "supergroup"):
        if not await get_group(chat.id):
            await add_group(chat.id, chat.title)

        await message.answer_photo(
            photo=PHOTO_URL,
            caption=START_TEXT.format(user=user.get_mention(), bot=(await message.bot.me).first_name),
        )

    # If private chat
    else:
        buttons = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{(await message.bot.me).username}?startgroup=true"),
            InlineKeyboardButton("👥 Group", url="https://t.me/+5vPKU47S6HNiNjY1"),
            InlineKeyboardButton("🔄 Updates", url="https://t.me/Who_Cares_qt"),
            InlineKeyboardButton("ɢx ᴅᴀʀᴋ ʙᴏᴛs [🇮🇳]", url="https://t.me/dark_x_knight_musiczz_support")
        )

        await message.answer_photo(
            photo=PHOTO_URL,
            caption=START_TEXT.format(user=user.get_mention(), bot=(await message.bot.me).first_name),
            reply_markup=buttons
        )