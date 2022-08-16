from re import T
from get_members import get_all_members, get_chat_id
from pyrogram.enums import UserStatus, ChatMemberStatus
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from random import randint
import asyncio

async def preclean_chat(link, settings, bot, message):
    chat_id = await get_chat_id(link=link)

    i = 0
    without_photo = []
    deleted = []
    last_week = []
    last_mounth = []
    long_ago = []
    
    all_users = await get_all_members(link)
    for member in all_users:
        
        if member.status == ChatMemberStatus.MEMBER:
            if settings["without_photo"] == True:
                if member.user.photo:
                    pass
                else:
                    without_photo.append(member)
            if settings["deleted_accs"] == True:
                if member.user.is_deleted:
                    deleted.append(member)
            if settings["last_week"] == True:
                if member.user.status == UserStatus.LAST_WEEK:
                    last_week.append(member)
            if settings["last_mounth"] == True:
                if member.user.status  == UserStatus.LAST_MONTH:
                    last_mounth.append(member)
            if settings["long_ago"] == True:
                if member.user.status  == UserStatus.LONG_AGO:
                    long_ago.append(member)
        else:
            
            pass
    await message.answer(f"Будет удалено:\n\nУдалённые аккаунты - {len(deleted)}\nБыли очень давно - {len(long_ago)}\nБез фото - {len(without_photo)}\nБыли на прошлой неделе - {len(last_week)}\nБыли в прошлом месяце - {len(last_mounth)}\n\nОжидайте завершения.", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Начать чистить чат", callback_data="start_clean")))
    
async def clean_chat(link, settings, bot, message):
    chat_id = await get_chat_id(link=link)

    i = 0
    without_photo = []
    deleted = []
    last_week = []
    last_mounth = []
    long_ago = []
    
    all_users = await get_all_members(link)
    for member in all_users:
        
        if member.status == ChatMemberStatus.MEMBER:
            if settings["without_photo"] == True:
                if member.user.photo:
                    pass
                else:
                    without_photo.append(member)
            if settings["deleted_accs"] == True:
                if member.user.is_deleted:
                    deleted.append(member)
            if settings["last_week"] == True:
                if member.user.status == UserStatus.LAST_WEEK:
                    last_week.append(member)
            if settings["last_mounth"] == True:
                if member.user.status  == UserStatus.LAST_MONTH:
                    last_mounth.append(member)
            if settings["long_ago"] == True:
                if member.user.status  == UserStatus.LONG_AGO:
                    long_ago.append(member)
        else:
            
            pass
    fails = 0
    success = 0
    to_kick = list(set(deleted + without_photo + last_week + last_mounth + long_ago))
    for member in to_kick:
        try:
            await bot.kick_chat_member(chat_id, member.user.id)
            success += 1
            await asyncio.sleep(randint(5, 10))
        except: fails += 1

    await message.answer(f"Успешно удалено - {success}\nНе вышло удалить - {fails}")
    