from telethon import events, TelegramClient
import os
import asyncio
import time 

api_id = 23478626
api_hash = 'aa37658f7437fc697396f72b2b4e3384'
guessSolver = TelegramClient('temp', api_id, api_hash)
chatid = -1002030874652#change
from telethon.tl.types import PhotoStrippedSize
ownerid = 2
last_guess_time = 0
GUESS_TIMEOUT = 10
@guessSolver.on(events.NewMessage(from_users=ownerid, pattern=".bin",outgoing=True))
async def guesser(event):
    await guessSolver.send_message(entity=chatid,message='/guess')
    for i in range(1,3000):
        await asyncio.sleep(300)
@guessSolver.on(events.NewMessage(from_users=572621020, pattern="Who's that pokemon?",chats=(int(chatid)),incoming=True))
async def guesser(event):
    for size in event.message.photo.sizes:
        if isinstance(size, PhotoStrippedSize):
            size = str(size)
            for file in (os.listdir("cache/")):
                with open(f"cache/{file}", 'r') as f:
                    file_content = f.read()
                if file_content == size:
                     chat = await event.get_chat()
                     await guessSolver.send_message(chat, f"{(file).split('.txt')[0]}")
            with open("cache.txt", 'w') as file:
                file.write(size)
            file.close()
                         
@guessSolver.on(events.NewMessage(from_users=572621020, pattern="The pokemon was ",chats=int(chatid)))
async def guesser(event):
    massage = ((event.message.text).split("The pokemon was **")[1]).split("**")[0]
    with open(f"cache/{massage}.txt", 'w') as file:
        with open("cache.txt",'r') as inf:
            cont = inf.read()
            file.write(cont)
        inf.close()
    file.close()
    os.remove("cache.txt")
    chat = await event.get_chat()
    await guessSolver.send_message(chat, "/guess")
    
async def check_response_timeout():
    global last_guess_time
    
    while True:
        current_time = time.time()
        if current_time - last_guess_time > GUESS_TIMEOUT:
            await guessSolver.send_message(entity=chatid, message='/guess')
            last_guess_time = current_time

        await asyncio.sleep(5)  # Check every 10 seconds

guessSolver.start()
guessSolver.loop.create_task(check_response_timeout())
guessSolver.run_until_disconnected()
