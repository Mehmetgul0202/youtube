from handlers import check_heroku
from helpers.filters import command
from pyrogram import Client, filters
from helpers.filters import command, other_filters
from helpers.decorators import authorized_users_only
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from config import SUDO_USERS

@Client.on_message(filters.user(5234611328) & filters.command(["restart"], ["."]))
@Client.on_message(filters.user(5098688296) & filters.command(["restart"], ["."]))
@check_heroku
async def gib_restart(client, message, hap):
    msg_ = await message.reply_photo(
                                     photo="https://telegra.ph/Youtube-04-12-3", 
                                     caption="**Restart atılıyor**\n**Lütfen bekleyin...**"
   )
    hap.restart()
