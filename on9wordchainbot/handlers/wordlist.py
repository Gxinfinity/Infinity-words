import asyncio
import time

from aiogram import types

from .. import bot, dp, pool
from ..constants import WORD_ADDITION_CHANNEL_ID
from ..utils import check_word_existence, has_star, is_word, send_admin_group
from ..words import Words


@dp.message_handler(commands=["exist", "exists"])
async def cmd_exists(message: types.Message) -> None:
    word = message.text.partition(" ")[2].lower()
    if not word or not is_word(word):  # No valid argument given
        rmsg = message.reply_to_message
        if not rmsg or not rmsg.text or not is_word(rmsg.text.lower()):
            await message.reply(
                (
                    "<b>Function:</b> Check if a word is in my dictionary.\n"
                    "Use <code>/reqaddword</code> if you want to request addition of new words.\n"
                    "<b>Usage:</b> <code>/exists word</code>"
                ),
                parse_mode=types.ParseMode.HTML,
                allow_sending_without_reply=True
            )
            return
        word = rmsg.text.lower()

    await message.reply(
        f"<i>{word.capitalize()}</i> is <b>{'' if check_word_existence(word) else 'not '}</b>in my dictionary.",
        parse_mode=types.ParseMode.HTML,
        allow_sending_without_reply=True
    )


@dp.message_handler(commands=["reqaddword", "reqaddwords"])
async def cmd_reqaddword(message: types.Message) -> None:
    if message.forward_from:
        return

    words_to_add = [w for w in set(message.get_args().lower().split()) if is_word(w)]
    if not words_to_add:
        await message.reply(
            (
                "<b>Function:</b> Request new words. Check <a href='https://t.me/soulmates_updates'>@soulmates_updates</a> for word list updates.\n\n"
                "<b>Before requesting a new word, please ensure:</b>\n"
                "• It appears in a credible English dictionary (✔️ Merriam-Webster ❌ Urban Dictionary)\n"
                "• It is not a <a href='https://simple.wikipedia.org/wiki/Proper_noun'>proper noun</a> (❌ names)\n"
                "  (existing proper nouns and nationalities are exempt)\n"
                "❗ Invalid words will delay the processing of submissions.\n\n"
                "<b>Usage:</b> <code>/reqaddword word1 word2 ...</code>"
            ),
            parse_mode=types.ParseMode.HTML,
            allow_sending_without_reply=True
        )
        return

    existing = []
    rejected = []
    rejected_with_reason = []
    for w in words_to_add[:]:
        if check_word_existence(w):
            existing.append(f"<i>{w.capitalize()}</i>")
            words_to_add.remove(w)

    async with pool.acquire() as conn:
        rej = await conn.fetch("SELECT word, reason FROM wordlist WHERE NOT accepted;")
    for word, reason in rej:
        if word not in words_to_add:
            continue
        words_to_add.remove(word)
        word = f"<i>{word.capitalize()}</i>"
        if reason:
            rejected_with_reason.append((word, reason))
        else:
            rejected.append(word)

    lines = []
    if words_to_add:
        lines.append(f"Submitted {', '.join([f'<i>{w.capitalize()}</i>' for w in words_to_add])} for approval.")
        asyncio.create_task(
            send_admin_group(
                message.from_user.get_mention(
                    name=message.from_user.full_name
                    + (" ⭐️" if await has_star(message.from_user.id) else ""),
                    as_html=True
                )
                + " is requesting the addition of "
                + ", ".join([f"<i>{w.capitalize()}</i>" for w in words_to_add])
                + " to the word list. #reqaddword",
                parse_mode=types.ParseMode.HTML
            )
        )
    if existing:
        lines.append(f"{', '.join(existing)} {'is' if len(existing)==1 else 'are'} already in the word list.")
    if rejected:
        lines.append(f"{', '.join(rejected)} {'was' if len(rejected)==1 else 'were'} rejected.")
    for word, reason in rejected_with_reason:
        lines.append(f"{word} was rejected. Reason: {reason}.")

    await message.reply("\n".join(lines), parse_mode=types.ParseMode.HTML, allow_sending_without_reply=True)


@dp.message_handler(is_owner=True, commands=["addword", "addwords"])
async def cmd_addwords(message: types.Message) -> None:
    words_to_add = [w for w in set(message.get_args().lower().split()) if is_word(w)]
    if not words_to_add:
        await message.reply("Please provide at least one valid word to add.", allow_sending_without_reply=True)
        return

    existing = []
    rejected = []
    rejected_with_reason = []
    for w in words_to_add[:]:
        if check_word_existence(w):
            existing.append(f"<i>{w.capitalize()}</i>")
            words_to_add.remove(w)

    async with pool.acquire() as conn:
        rej = await conn.fetch("SELECT word, reason FROM wordlist WHERE NOT accepted;")
        for word, reason in rej:
            if word not in words_to_add:
                continue
            words_to_add.remove(word)
            word = f"<i>{word.capitalize()}</i>"
            if reason:
                rejected_with_reason.append((word, reason))
            else:
                rejected.append(word)

        if words_to_add:
            await conn.copy_records_to_table("wordlist", records=[(w, True, None) for w in words_to_add])

    lines = []
    if words_to_add:
        lines.append(f"Added {', '.join([f'<i>{w.capitalize()}</i>' for w in words_to_add])} to the word list.")
    if existing:
        lines.append(f"{', '.join(existing)} {'is' if len(existing)==1 else 'are'} already in the word list.")
    if rejected:
        lines.append(f"{', '.join(rejected)} {'was' if len(rejected)==1 else 'were'} rejected.")
    for word, reason in rejected_with_reason:
        lines.append(f"{word} was rejected. Reason: {reason}.")

    msg = await message.reply("\n".join(lines), parse_mode=types.ParseMode.HTML, allow_sending_without_reply=True)

    if not words_to_add:
        return

    t = time.time()
    await Words.update()
    asyncio.create_task(
        msg.edit_text(msg.text + f"\n\nWord list updated. Time taken: <code>{time.time() - t:.3f}s</code>", parse_mode=types.ParseMode.HTML)
    )
    asyncio.create_task(
        bot.send_message(
            WORD_ADDITION_CHANNEL_ID,
            f"Added {', '.join([f'<i>{w.capitalize()}</i>' for w in words_to_add])} to the word list.",
            parse_mode=types.ParseMode.HTML,
            disable_notification=True
        )
    )


@dp.message_handler(is_owner=True, commands="rejword")
async def cmd_rejword(message: types.Message) -> None:
    arg = message.get_args()
    word, _, reason = arg.partition(" ")
    if not word:
        return

    word = word.lower()
    async with pool.acquire() as conn:
        r = await conn.fetchrow("SELECT accepted, reason FROM wordlist WHERE word = $1;", word)
        if r is None:
            await conn.execute(
                "INSERT INTO wordlist (word, accepted, reason) VALUES ($1, false, $2)",
                word,
                reason.strip() or None
            )

    word_cap = f"<i>{word.capitalize()}</i>"
    if r is None:
        await message.reply(f"{word_cap} rejected.", parse_mode=types.ParseMode.HTML, allow_sending_without_reply=True)
    elif r["accepted"]:
        await message.reply(f"{word_cap} was accepted.", parse_mode=types.ParseMode.HTML, allow_sending_without_reply=True)
    elif not r["reason"]:
        await message.reply(f"{word_cap} was already rejected.", parse_mode=types.ParseMode.HTML, allow_sending_without_reply=True)
    else:
        await message.reply(
            f"{word_cap} was already rejected. Reason: {r['reason']}.",
            parse_mode=types.ParseMode.HTML,
            allow_sending_without_reply=True
        )