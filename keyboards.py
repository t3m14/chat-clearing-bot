from email import message
from gc import callbacks
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from db import get_all_keys



delete_menu = KeyboardButton("Удаление")
keys_button = KeyboardButton("Ключи")
help_button = KeyboardButton("Помощь")
main_kb = ReplyKeyboardMarkup().add(delete_menu).add(keys_button, help_button)
def get_keys_kb(message_id):
    keys_kb = InlineKeyboardMarkup()
    for key in get_all_keys():
        if key.split(" - ")[0] != "":
            keys_kb.add(InlineKeyboardButton(text=key, callback_data=key.split(" - ")[-1]+"~deletekey"))
    keys_kb.add(InlineKeyboardButton(text="Создать новый ключ", callback_data="create_new_key"))
    keys_kb.add(InlineKeyboardButton(text="❌", callback_data=f"close_keys_menu~{message_id}"))
    return keys_kb


clear_settings_kb = InlineKeyboardMarkup()






deleted_acc_btn = InlineKeyboardButton(text="❎ Удалённые аккаунты", callback_data="deleted_acc-setting~inactive")
without_photo_btn = InlineKeyboardButton(text="❎ Аккаунты без фото", callback_data="wihout_photo-setting~inactive")
last_week_btn = InlineKeyboardButton(text="❎ Аккаунты, неактивные больше недели", callback_data="last_week-setting~inactive")
last_mounth_btn = InlineKeyboardButton(text="❎ Аккаунты, неактивные больше месяца", callback_data="last_mounth-setting~inactive")
long_ago_btn = InlineKeyboardButton(text="❎ Аккаунты, неактивные очень давно", callback_data="long_ago-setting~inactive")
clear_settings_kb.add(deleted_acc_btn).add(without_photo_btn).add(last_week_btn).add(last_mounth_btn).add(long_ago_btn)