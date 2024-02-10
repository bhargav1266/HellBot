from telethon import events, TelegramClient
from asyncio import sleep as zzz
import asyncio
import time

api_id = 23478626
api_hash = 'aa37658f7437fc697396f72b2b4e3384'
bot = TelegramClient('session', api_id, api_hash)

list = ["lugia", "Daily", "kyogre", "rayquaza", "groudon"]
hunt = False
last_hunt_time = 0
HUNT_TIMEOUT = 2
chat_id = '@Shiny_catcher_bot'
response_chat_id = '@Shiny_catcher_bot' 

hexa_id = '@Hexamonbot'
@bot.on(events.NewMessage(outgoing=True, pattern='.go'))
async def begin(event):
    chat = await event.get_chat()
    global hunt
    hunt = True
    await bot.send_message(hexa_id, "/hunt")

@bot.on(events.NewMessage(chats=572621020, incoming=True))
async def hunt(event):
    if hunt:
        chat = await event.get_chat()
        text = event.message.text
        hun = True
        if "Shiny" in text:
            await bot.send_message(chat_id, 'SHINY FOUND!')
            await bot.disconnect()
        elif "TM" in text:
            await zzz(0.8)
            await bot.send_message(chat, "/hunt")
        elif any(item in text for item in list):
         
            response_message = "Pokemon found->  {}".format(text)
            await bot.send_message(response_chat_id, response_message)
            await bot.disconnect()
      
                

async def check_response_timeout():
    global last_hunt_time

    while True:
        current_time = time.time()
        if current_time - last_hunt_time > HUNT_TIMEOUT:
            await bot.send_message(hexa_id, '/hunt')
            last_hunt_time = current_time

        await asyncio.sleep(2)

@bot.on(events.NewMessage(outgoing=True, pattern='.stop'))
async def stop(event):
    global hunt
    hunt = False

bot.start()
bot.loop.create_task(check_response_timeout())
bot.run_until_disconnected()