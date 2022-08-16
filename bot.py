import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram_dialog import DialogRegistry
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Checkbox, ManagedCheckboxAdapter
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import Dialog
from aiogram_dialog import DialogManager, StartMode, ChatEvent

from config import TOKEN, admin_id
from keyboards import main_kb, clear_settings_kb, get_keys_kb
from db import add_key, chek_is_key_exist, delete_key, get_key_by_username
from delete_users import clean_chat, preclean_chat
chat_link = ""
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class States(StatesGroup):
    wait_for_key = State()
    main_menu = State()
    clear_settings = State()
clear_stgs = {
    "deleted_accs" : False,
    "without_photo" : False,
    "last_week" : False,
    "last_mounth" : False,
    "long_ago" : False
}
async def deleted_accs(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    global clear_stgs
    clear_stgs["deleted_accs"] = checkbox.is_checked()
    print(clear_stgs["deleted_accs"])
async def without_photo(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    global clear_stgs
    clear_stgs["without_photo"] = checkbox.is_checked()
async def last_week(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    global clear_stgs
    clear_stgs["last_week"] = checkbox.is_checked()
async def last_mounth(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    global clear_stgs
    clear_stgs["last_mounth"] = checkbox.is_checked()
async def long_ago(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    global clear_stgs
    clear_stgs["long_ago"] = checkbox.is_checked()
    
async def start_clean(call: types.CallbackQuery, button: Button, manager: DialogManager):
    global chat_link
    global clear_stgs
    await preclean_chat(chat_link, clear_stgs, bot, call.message)
    await manager.done()
    await call.message.delete()
    await States.main_menu.set()
    
async def back_to_main_menu(call: types.CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()
    await call.message.delete()
    await States.main_menu.set()
    global clear_stgs
    clear_stgs = {
    "deleted_accs" : False,
    "without_photo" : False,
    "last_week" : False,
    "last_mounth" : False,
    "long_ago" : False
    }
@dp.message_handler(state=States.clear_settings)
async def clear_settings_func(message: types.Message, dialog_manager: DialogManager):
    if "/" and "." in message.text:
        global chat_link
        chat_link = message.text
        await message.delete()
        try:
            await bot.delete_message(message.chat.id, message.message_id - 1 )
        except:
            try:
                await bot.delete_message(message.chat.id, message.message_id - 2)
            except: pass
        await dialog_manager.start(States.clear_settings)
    else:
        await bot.delete_message(message.chat.id, message.message_id)

registry = DialogRegistry(dp)  # this is required to use `aiogram_dialog`
main_window = Window(
    Const("Выберете настройки очистки \nЧтобы закрыть нажмите ❌"),  # just a constant text
    Checkbox(
    Const("✅ Удалённые аккаунты"),
    Const("❎  Удалённые аккаунты"),
    id="deleted_accs",
    default=False,  # so it will be checked by default,
    on_state_changed=deleted_accs,
    ),
    Checkbox(
    Const("✅ Аккаунты без аватарок"),
    Const("❎ Аккаунты без аватарок"),
    id="without_photo",
    default=False,  # so it will be checked by default,
    on_state_changed=without_photo,
    ),
    Checkbox(
    Const("✅ Неактивен больше недели"),
    Const("❎ Неактивен больше недели"),
    id="last_week",
    default=False,  # so it will be checked by default,
    on_state_changed=last_week,
    ),
    Checkbox(
    Const("✅ Неактивен больше месяца"),
    Const("❎ Неактивен больше месяца"),
    id="last_mounth",
    default=False,  # so it will be checked by default,
    on_state_changed=last_mounth,
    ),
    Checkbox(
    Const("✅ Неактивен очень давно"),
    Const("❎ Неактивен очень давно"),
    id="long_ago",
    default=False,  # so it will be checked by default,
    on_state_changed=long_ago,
    ),
    Button(Const("Продолжить"), id="clean", on_click=start_clean),
    Button(Const("❌"), id="exit_to_menu", on_click=back_to_main_menu),
    # button with text and id
    state=States.clear_settings,# state is used to identify window between dialogs
    )

dialog = Dialog(main_window)
registry.register(dialog)  # register a dialog



@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message):
    print(clear_stgs)
    if message.chat.id == admin_id or get_key_by_username(message.from_user.username):
        await message.answer("Выберете нужный пункт меню.", reply_markup=main_kb)
        await States.main_menu.set()
    else:
        await message.answer("Введите ключ доступа")
        await States.wait_for_key.set()
@dp.message_handler(state=States.wait_for_key)
async def check_key(message: types.Message):
    if chek_is_key_exist(message.from_user.username, message.text):
        await message.answer("Выберете нужный пункт меню.", reply_markup=main_kb)
        await States.main_menu.set()
    else:
        await message.answer("Неверный ключ")
        
@dp.message_handler(state=States.main_menu)
async def main_menu(message: types.Message):
    if get_key_by_username(message.from_user.username) == "":
        if message.from_user.id == admin_id:
            if message.text == "Удаление":
                await message.answer("Отправьте ссылку на чат")
                await bot.delete_message(message.from_user.id, message.message_id)
                await States.clear_settings.set()
            elif message.text == "Ключи":
                if message.from_user.id == admin_id:
                    await message.answer("Ключи доступа:\n\nДля удаления ключа нажмите на него. \n Чтобы закрыть нажмите ❌", reply_markup=get_keys_kb(message.message_id))
                else:
                    await message.answer(f"Ваш ключ - {get_key_by_username(message.from_user.username)}.")
            elif message.text == "Помощь":
                await message.answer("Бот должен обязательно находится в чате и иметь все необходимые права для администрирования чата.", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Понятно", callback_data=f"help_ok~{message.message_id}")))
        else:
            await message.answer("Вы были исключены администратором.")
    elif message.text == "Удаление":
        await message.answer("Отправьте ссылку на чат")
        await bot.delete_message(message.from_user.id, message.message_id)
        await States.clear_settings.set()
    elif message.text == "Ключи":
        if message.from_user.id == admin_id:
            await message.answer("Ключи доступа:\n\nДля удаления ключа нажмите на него. \n Чтобы закрыть нажмите ❌", reply_markup=get_keys_kb(message.message_id))
        else:
            await message.answer(f"Ваш ключ - {get_key_by_username(message.from_user.username)}.")
    elif message.text == "Помощь":
        await message.answer("Бот должен обязательно находится в чате и иметь все необходимые права для администрирования чата.", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Понятно", callback_data=f"help_ok~{message.message_id}")))




@dp.callback_query_handler(state="*")
async def callbacks(call: types.CallbackQuery):
    if "help_ok" in call.data:
        await bot.delete_message(call.message.chat.id, call.data.split("~")[-1])
        await call.message.delete()
        await States.main_menu.set()
    if call.data == "create_new_key":
        msg = await call.message.answer(text=f"Поделитесь этим ключом с новым пользователем.\n\n{add_key()}\n\nКлюч вводится при регистрации, после команды /start\n(Сообщение исчезнет через 10 секунд)")
        await asyncio.sleep(10)
        await msg.delete()
    if "close_keys_menu" in call.data:
        await bot.delete_message(call.message.chat.id, call.data.split("~")[-1])
        await call.message.delete()
        await States.main_menu.set()
    if "deletekey" in call.data:
        to_delete = call.data.split("~")[0]
        delete_key(to_delete)
        await call.answer(text=f"Ключ {to_delete}, был удалён.", show_alert=True)
        await call.message.edit_text(call.message.text, reply_markup=get_keys_kb(call.message.message_id-1))
    if call.data == "start_clean":
        global chat_link
        global clear_stgs
        await clean_chat(chat_link, clear_stgs, bot, call.message)
        clear_stgs = {
        "deleted_accs" : False,
        "without_photo" : False,
        "last_week" : False,
        "last_mounth" : False,
        "long_ago" : False
        }
        await call.message.delete()
        
if __name__ == '__main__':
    executor.start_polling(dp)