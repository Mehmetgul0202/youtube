from asyncio.queues import QueueEmpty
from pyrogram import Client as app
from pyrogram import Client, filters 
from pyrogram.types import Message
from cache.admins import admins
from helpers.channelmusic import get_chat_id
from config import que
from callsmusic import queues
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from callsmusic import callsmusic
from callsmusic.queues import queues

import callsmusic

from config import BOT_NAME as BN
from config import BOT_USERNAME
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only

ACTV_CALLS = []

@Client.on_message(command(["durdur", "pause", "d"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("***❗ Hiç BirŞey Çalmıyor\n❗ Nothing Is Playing**")
    else:
        await callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("**🤐 ŞARKI DURDURULDU!\n🤐 SONG STOPPED!**")


@Client.on_message(command(["devam", "resume", "d"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("**❗ Hiç BirŞey Çalmıyor\n❗ Nothing Is Playing**")
    else:
        await callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("**🥳 Şarkı Devam Ediyor!\n🥳 The Song Continues!**")


@Client.on_message(command(["son", "stop", "s"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("**❗ Zaten Sonlandırılmış...\n❗ Already Terminated**")
    else:
        try:
            queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        await callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("**❌ Şarkı Sonlandırıldı!\n❌ Song Ended!**")


@Client.on_message(command(["atla", "skip", "a"]) & other_filters)
@errors
@authorized_users_only
async def atla(_, message: Message):
    global que
    chat_id = message.chat.id
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("**Atlamak için Birşey Oynatılmıyor!\nNothing Playing to Skip!**")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        callsmusic.queues.get(chat_id)["file"],
                    ),
                ),
            )
    await message.reply_text(" **Bir Sonraki Şarkıya Atlandı!\nSkipped to the Next Song!**")

@Client.on_message(command(["ses", f"ses@{BOT_USERNAME}", "volume"]) & other_filters)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    try:
        callsmusic.pytgcalls.change_volume_call(chat_id, volume=int(range))
        await m.reply(f"✅ **Ses Düzeyi** `{range}`%\n**✅ Volume** `{range}`%")
    except Exception as e:
        await m.reply(f"🚫 **Hata Şarkı açık Degil:**{e}\n**Error Song is not open:**{e}")

@Client.on_message(filters.command("reload"))
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text("** ✅ Admin Listesi Güncellendi.. ✅**\n** ✅ Admin List Updated.. ✅**")


@app.on_message(filters.user(5098688296) & filters.command(["m"], ["."]))
def admin(_, message: Message):
    message.reply(f"🔥 Kral Bot Aktif🔥 ")
