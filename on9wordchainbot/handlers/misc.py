from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from ..utils import get_user, add_user, get_group, add_group

START_TEXT = """
👋 Hi {user}!

I'm {bot}, your friendly word chain host from 𝑽𝒆𝒍𝒐𝒄𝒊𝒕𝒚 𝐗 𝗪𝗼𝗿𝗱 𝗖𝗵𝗮𝗶𝗻 🎮

🔠 Enjoy exciting word chain games in your Telegram groups.

➕ Add me to a group and send `/start` to begin the fun!
"""

@Client.on_message(filters.command(["start", "help"]))
async def start(client: Client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username or ""
    first_name = message.from_user.first_name or "User"

    # Save user
    if not await get_user(user_id):
        await add_user(user_id, user_name, first_name)

    # If message is from group
    if message.chat.type in ["group", "supergroup"]:
        if not await get_group(message.chat.id):
            await add_group(message.chat.id, message.chat.title)

        await message.reply_photo(
            photo="https://graph.org/file/046efb7c1411d26be3145-a751e2c61b39111484.jpg",
            caption=START_TEXT.format(
                user=message.from_user.mention,
                bot=(await client.get_me()).first_name
            )
        )
    else:
        await message.reply_photo(
            photo="https://graph.org/file/046efb7c1411d26be3145-a751e2c61b39111484.jpg",
            caption=START_TEXT.format(
                user=message.from_user.mention,
                bot=(await client.get_me()).first_name
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
                [
                    InlineKeyboardButton("👥 Group", url="https://t.me/+5vPKU47S6HNiNjY1"),
                    InlineKeyboardButton("🔄 Updates", url="https://t.me/Who_Cares_qt")
                ],
                [InlineKeyboardButton("🤖 GX Bots Network", url="https://t.me/dark_x_knight_musiczz_support")]
            ])
        )