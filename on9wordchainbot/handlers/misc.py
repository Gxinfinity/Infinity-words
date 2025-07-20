from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from ..utils import get_user, add_user, get_group, add_group

START_TEXT = """
Hi👋 {user}!

I'm {bot} – your fun companion from 𝑽𝒆𝒍𝒐𝒄𝒊𝒕𝒚 𝐗 𝗪𝗼𝗿𝗱 𝗖𝗵𝗮𝗶𝗻 🎮

Play exciting word chain games with your friends in Telegram groups.
➕ Add me to a group and type `/start` to begin the fun!
"""

@Client.on_message(filters.command(["start", "help"]))
async def start_command(client: Client, message: Message):
    user = message.from_user
    chat = message.chat

    # Save user
    if not await get_user(user.id):
        await add_user(user.id, user.username or "", user.first_name or "")

    # Group handling
    if chat.type in ["group", "supergroup"]:
        if not await get_group(chat.id):
            await add_group(chat.id, chat.title)

        await message.reply_photo(
            photo="https://graph.org/file/046efb7c1411d26be3145-a751e2c61b39111484.jpg",
            caption=f"👋 Hello {user.mention}, I'm ready to play word chain in *{chat.title}*! 🎮\nUse `/play` to begin!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ℹ️ Help", url=f"https://t.me/{(await client.get_me()).username}?start=help")]
            ])
        )

    # Private (DM) handling
    else:
        await message.reply_photo(
            photo="https://graph.org/file/046efb7c1411d26be3145-a751e2c61b39111484.jpg",
            caption=START_TEXT.format(
                user=user.mention,
                bot=(await client.get_me()).first_name
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
                [
                    InlineKeyboardButton("👥 Group", url="https://t.me/+5vPKU47S6HNiNjY1"),
                    InlineKeyboardButton("🔄 Updates", url="https://t.me/Who_Cares_qt")
                ],
                [InlineKeyboardButton("ɢx ᴅᴀʀᴋ ʙᴏᴛs [🇮🇳]", url="https://t.me/dark_x_knight_musiczz_support")]
            ])
        )