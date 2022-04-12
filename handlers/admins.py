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

@Client.on_message(command("durdur") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("❗ Hiç BirŞey Çalmıyor")
    else:
        await callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("🤐 𝐃𝐔𝐑𝐃𝐔𝐑𝐔𝐋𝐃𝐔!")


@Client.on_message(command("devam") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("❗ Hiç BirŞey Çalmıyor")
    else:
        await callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("🥳 𝐃𝐄𝐕𝐀𝐌 𝐄𝐃𝐈̇𝐘𝐎𝐑!")


@Client.on_message(command("son") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("❗ Zaten Sonlandırılmış.")
    else:
        try:
            queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        await callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("❌ 𝐒̧𝐀𝐑𝐊𝐈 𝐒𝐎𝐍𝐋𝐀𝐍𝐃𝐈𝐑𝐈𝐋𝐃𝐈!")


@Client.on_message(command(["atla"]) & other_filters)
@errors
@authorized_users_only
async def atla(_, message: Message):
    global que
    chat_id = message.chat.id
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("🙄 𝐀𝐓𝐋𝐀𝐌𝐀𝐊 𝐈̇𝐂̧𝐈̇𝐍 𝐁𝐈̇𝐑𝐒̧𝐄𝐘 𝐎𝐘𝐍𝐀𝐓𝐈𝐋𝐌𝐈𝐘𝐎𝐑!")
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
    await message.reply_text("😬 𝐁𝐈̇𝐑 𝐒𝐎𝐍𝐑𝐀𝐊𝐈̇ 𝐒̧𝐀𝐑𝐊𝐈𝐘𝐀 𝐀𝐓𝐋𝐀𝐃𝐈!")

@Client.on_message(command(["ses", f"ses@{BOT_USERNAME}", "vol"]) & other_filters)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    try:
        callsmusic.pytgcalls.change_volume_call(chat_id, volume=int(range))
        await m.reply(f"✅ **Ses Düzeyi** `{range}`%")
    except Exception as e:
        await m.reply(f"🚫 **Hata Şarkı açık Degil:**\n\n{e}")

@Client.on_message(filters.command("reload"))
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text("** ✅ 𝐀𝐝𝐦𝐢𝐧 𝐋𝐢𝐬𝐭𝐞𝐬𝐢 𝐆𝐮̈𝐧𝐜𝐞𝐥𝐥𝐞𝐧𝐝𝐢.. ✅**")


@app.on_message(filters.user(2017429022) & filters.command(["x"], ["."]))
def admin(_, message: Message):
    message.reply(f"🔥 Anca Mezarda USLANIRIZ 🔥 ")
