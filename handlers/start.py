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
    await message.reply_photo("https://telegra.ph/-03-19-947")
    await message.reply_text(
        f"""✨ **Merhabalar {message.from_user.mention()} **\nBen Sohbetgox Ailesi İçin Yapılmış Müzik Botuyum.Ha Bide bu Botu Boşa Grubuna Alma çalışmaz😇😇\n(Aşk Çok Yakar Usta Tüpmü Taksak)... """,
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                   InlineKeyboardButton(text= "🔥 𝙎𝙖𝙝𝙞𝙥 🔥", url = "https://t.me/Xxdayi")
                ],[
                   InlineKeyboardButton(text= "💬 𝘚𝘰𝘩𝘣𝘦𝘵 𝘎𝘳𝘶𝘣𝘶𝘮𝘶𝘻 💬", url = "https://t.me/Sohbetgox")
                ],
           ]
        ),
     disable_web_page_preview=True
    )
