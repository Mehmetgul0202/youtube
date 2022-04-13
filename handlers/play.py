import os
from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch
import converter
from downloaders import youtube
from config import DURATION_LIMIT
from helpers.filters import command
from helpers.decorators import errors, authorized_users_only
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()





@Client.on_message(command(["play", "oynat"]) 
                   & filters.group
                   & ~filters.edited 
                   & ~filters.forwarded
                   & ~filters.via_bot)
@errors
@authorized_users_only
async def play(_, message: Message):

    lel = await message.reply("🔄 **ʟüᴛꜰᴇɴ ʙᴇᴋʟᴇʏiɴiᴢ...**")
    
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "youtubeVcAsistan"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>Önce beni Grubunun yöneticisi olarak ekle!</b>\n<b>First add me as admin of your Group!</b>")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**Asistan Davetiniz üzerine katıldı\nAssistant joined upon your invitation**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>🛑 Taşan Bekleme Hatası 🛑</b> \n\Merhaba {user.first_name}, yardımcı userbot, yoğun katılma istekleri nedeniyle grubunuza katılamadı. Userbot'un grupta yasaklı olmadığından emin olun ve daha sonra yeniden deneyin!")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>{user.first_name}, @youtubevcasistan Grupunuzdan Banlanmis veya Çıkartılmıştır.Lütfen Bani Kaldırıp Tekrar Deneyiniz.</i>\n@youtubevcasistan Banned or Removed From Your Group. Please Remove Ban And Try Again.")
        return
    
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**❌ Daha uzun videolar {DURATION_LIMIT} dakikaların oynatılamasına izin verilmez!\n❌ Longer videos {DURATION_LIMIT} minutes are not allowed to be played!**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://i.ibb.co/Qkz78hx/images-1.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Yerel olarak eklendi"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📜 𝙆𝙤𝙢𝙪𝙩𝙡𝙖𝙧 𝙑𝙚 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 📜",
                        url="https://t.me/youtubevcdestek")
                   
                ]
            ]
        )
        
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")
            
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
            keyboard = InlineKeyboardMarkup(
             [
                   [
                    InlineKeyboardButton(
                        text="📜 𝙆𝙤𝙢𝙪𝙩𝙡𝙖𝙧 𝙑𝙚 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 📜",
                        url="https://t.me/youtubevcdestek")
                   
                   ]
            ]
        )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://i.ibb.co/Qkz78hx/images-1.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                  [
                    InlineKeyboardButton(
                        text="📜 𝙆𝙤𝙢𝙪𝙩𝙡𝙖𝙧 𝙑𝙚 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 📜",
                        url="https://t.me/youtubevcdestek")
                   
                  ]
            ]
        )
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"**❌ Daha uzun videolar {DURATION_LIMIT} dakikaların oynatılamasına izin verilmez!\n❌ Longer videos {DURATION_LIMIT} minutes are not allowed to be played!**")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("🧐 **Dinlemek istediğin şarkı nedir?\n🧐 What song do you want to listen to?**")
        await lel.edit("🙂")
        query = message.text.split(None, 1)[1]
        # print(query)
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
        except Exception as e:
            await lel.edit(
                "❌ Şarkı bulunamadı.\n\nBaşka bir şarkı deneyin veya belki düzgün heceleyin.\n❌ Song not found.\n\nTry another song or maybe spell it out properly."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
           [
                [
                    InlineKeyboardButton(
                        text="📜 𝙆𝙤𝙢𝙪𝙩𝙡𝙖𝙧 𝙑𝙚 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 📜",
                        url="https://t.me/youtubevcdestek")
                   
                ]
            ]
        )
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"**❌ Daha uzun videolar {DURATION_LIMIT} dakikaların oynatılamasına izin verilmez!\n❌ Longer videos {DURATION_LIMIT} minutes are not allowed to be played!**")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
  
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(message.chat.id) in ACTV_CALLS:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="https://telegra.ph/Youtube-04-12-38",
        caption="**🎵 : ** {}\n**🕒 :** {} min\n**👤 :** {}\n\n**🔸 𝐒̧𝐀𝐑𝐊𝐈 𝐒𝐈𝐑𝐀𝐘𝐀 𝐀𝐋𝐈𝐍𝐃𝐈:** {}".format(
        title, duration, message.from_user.mention(), position
        ),
        reply_markup=keyboard)
        return await lel.delete()
    else:
        await callsmusic.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
        photo="https://telegra.ph/Youtube-04-12-3",
        reply_markup=keyboard,
        caption="**🎵 :** {}\n**🕒 :** {} min\n**👤 :** {}\n**👥 : `{}`**".format(
        title, duration, message.from_user.mention(), message.chat.title
        ), )
        return await lel.delete()
