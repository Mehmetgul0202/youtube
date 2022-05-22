from time import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn
from helpers.filters import command, other_filters
from config import BOT_USERNAME, SUDO_USERS, BOT_NAME, ASSISTANT_NAME


__major__ = 0
__minor__ = 2
__micro__ = 1



START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)



@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_photo("https://telegra.ph/Youtube-04-12-3")
    await message.reply_text(
        f"""✨ **Merhabalar {message.from_user.mention()} **\n\nBen Sesli Sohbette Müzik Dinlemeniz İçin Yapıldım.\nGrubunuza alıp kullanabilirsiniz...\n\n✨ **Hello {message.from_user.mention()} **\n\nI'm Made For You To Listen To Music In Voice Chat.\nYou can use it in your group... """,
        reply_markup=InlineKeyboardMarkup(
            [ 
               [          
                   InlineKeyboardButton(
                        "🔥 SAHİP 🔥", url="https://t.me/MissSahip")
                ],[          
                   InlineKeyboardButton(
                        "🎶 𝘽𝙚𝙣𝙞 𝙂𝙧𝙪𝙗𝙪𝙣𝙖 𝙀𝙠𝙡𝙚 🎶", url="https://t.me/YoutubeVcBot?startgroup=a")
                ],[
                   InlineKeyboardButton(
                        "🥳 𝘼𝙨𝙞𝙨𝙩𝙖𝙣 🥳", url="https://t.me/YoutubeVcAsistan")
                ],[
                   InlineKeyboardButton(
                        "📜 𝙆𝙤𝙢𝙪𝙩𝙡𝙖𝙧 𝙑𝙚 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 📜", url="https://t.me/YoutubeVcDestek")  
                ],
           ]
        ),
     disable_web_page_preview=True
    )
