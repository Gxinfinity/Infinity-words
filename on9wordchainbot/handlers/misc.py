from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_TEXT = """
<b>Hi {user}!</b>

I’m <b>{bot}</b> – your word chain companion from <i>𝑽𝒆𝒍𝒐𝒄𝒊𝒕𝒚 𝐗</i> 🎮

➤ Add me to a Telegram group and type <code>/startclassic</code> to begin the fun!

🔤 Make chains, earn points, and climb the leaderboard!
"""

START_BUTTONS = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("➕ Add Me To Group", url="https://t.me/Velocityxrobot?startgroup=true")],
    [
        InlineKeyboardButton("👥 Group", url="https://t.me/+5vPKU47S6HNiNjY1"),
        InlineKeyboardButton("🔄 Updates", url="https://t.me/Who_Cares_qt")
    ],
    [InlineKeyboardButton("ɢx ᴅᴀʀᴋ ʙᴏᴛs [🇮🇳]", url="https://t.me/dark_x_knight_musiczz_support")]
])

@dp.message_handler(CommandStart(), ChatTypeFilter([types.ChatType.PRIVATE]))
async def cmd_start(message: types.Message) -> None:
    user = message.from_user.get_mention(as_html=True)
    bot_info = await bot.me

    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://graph.org/file/046efb7c1411d26be3145-a751e2c61b39111484.jpg",
        caption=START_TEXT.format(user=user, bot=bot_info.first_name),
        reply_markup=START_BUTTONS,
        parse_mode="HTML"
    )