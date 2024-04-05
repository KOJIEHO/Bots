import time
from pyrogram import Client
from pyrogram import filters
import aiofiles
import pathlib


pathlib.Path('users.txt').touch(exist_ok=True)
api_id = 
api_hash = ''
text = ''
app = Client(name='my_account', api_id=api_id, api_hash=api_hash)


@app.on_message(filters=filters.private)
async def auto_answer(event, message):
    async with aiofiles.open(file='users.txt', mode='r') as file:
        users = (await file.read()).split('\n')

    if str(message.chat.id) not in users:
        async with aiofiles.open(file='users.txt', mode='a+') as file:
            await file.write(f'{message.chat.id}\n')
            if message.from_user.id != (await app.get_me()).id:
                await app.send_message(chat_id=message.chat.id, text=text)
    time.sleep(120)

app.run()
