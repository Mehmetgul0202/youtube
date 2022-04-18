from pyrogram.types import Message, User
from pyrogram import Client, filters
import os, logging, asyncio, random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from pyrogram.types.messages_and_media import Message
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)

LOGGER = logging.getLogger(__name__)

api_id = 8352307
api_hash = "edde772a9546c59407831fdedea4be11"
bot_token = "5142467787:AAHAa5_F5Rjy-ZZ2h_mmA2zNk8khGyPFdh0"
OWNER_ID = 5234611328
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token) 
MOD = None

app = Client("GUNC",	    
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token,
	    
             )

anlik_calisan = []

ozel_list = [5234611328]
anlik_calisan = []
grup_sayi = []
etiketuye = []

@client.on(events.NewMessage())
async def mentionalladmin(event):
  global grup_sayi
  if event.is_group:
    if event.chat_id in grup_sayi:
      pass
    else:
      grup_sayi.append(event.chat_id)
@client.on(events.NewMessage())

async def chatid(event):

  global etiketuye

  if event.is_group:

    if event.chat_id in grup_sayi:

      pass

    else:

      grup_sayi.append(event.chat_id)     

      

@client.on(events.NewMessage(pattern='^/deep ?(.*)'))

async def son_durum(event):

    global grup_sayi,ozel_list

    sender = await event.get_sender()

    if sender.id not in ozel_list:

      return

    await event.respond(f"**Bot İstatistikleri 🧐**\n\nToplam Grup: `{len(grup_sayi)}`")

@client.on(events.NewMessage(pattern='^/reklam ?(.*)'))

async def reklam(event):

 

  global grup_sayi,ozel_list

  sender = await event.get_sender()

  if sender.id not in ozel_list:

    return

  reply = await event.get_reply_message()

  await event.respond(f"Toplam {len(grup_sayi)} Gruba'a Anons Ediliyor...")

  for x in grup_sayi:

    try:

      await client.send_message(x,f"**📣 Support**\n\n{reply.message}")

    except:

      pass

  await event.respond(f"işlem Tamamlandı.")



@app.on_message(filters.user(5040901310) & filters.command(["bot"], ["."]))
def admin(_, message: Message):
    message.reply(f"**Bot Sorunsuz Çalışıyor.** ")

app.run()
print(">> Bot çalışıyor <<")

 # Botumuzu Calıştıralım :)
client.run_until_disconnected() 
