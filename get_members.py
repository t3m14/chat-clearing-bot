from pyrogram import Client
from config import api_id, api_hash
async def get_all_members(chat_link):
    async with Client("89292394343", api_id, api_hash, workdir="./sessions/") as app:
        members_list = []
        chat = await app.get_chat(chat_link.split("/")[-1])
        members = app.get_chat_members(chat.id)
        async for member in members:
            members_list.append(member)
        await app.stop()
        return members_list
    
async def get_chat_id(link):
    async with Client("89292394343", api_id, api_hash, workdir="./sessions/") as app:
        chat = await app.get_chat(link.split("/")[-1])
        await app.stop()

        return chat.id