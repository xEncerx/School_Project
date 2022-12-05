from aiogram import types, Dispatcher
import markups as nav
from bot_data import bot, db, admin_id
from markups import cb
from utils.message_utils import text_editor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

class getAnswer(StatesGroup):
    answer = State()

async def admin_menu(call: types.CallbackQuery):
    await text_editor(text="Добро пожаловать в Админ Меню:", call=call, markup=nav.admin_menu())
    await call.answer()

async def add_delete_admin(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    match action:
        case "add_admin":
            await text_editor(text="Введите ID/Username пользователя:", call=call)
            await getAnswer.answer.set()
            await state.update_data(action="add")
        case "delete_admin":
            await text_editor(text="Введите ID/Username пользователя:", call=call)
            await getAnswer.answer.set()
            await state.update_data(action="delete")

async def action(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer"] = message.text
        a = await state.get_data()
    match a["action"]:
        case "add":
            if db.client_exist(data["answer"]):
                if data["answer"].isdigit():
                    await bot.send_message(message.from_user.id, f"Пользователь {data['answer']} был назначен администратором", reply_markup=nav.admin_menu())
                    db.update_data(int(data["answer"]), "role", "admin")
                else:
                    if db.client_exist(data["answer"]):
                        await bot.send_message(message.from_user.id, f"Пользователь {data['answer']} был назначен администратором", reply_markup=nav.admin_menu())
                        db.update_data(ID=data["answer"], place="username", data="role", value="admin")
            else:
                await bot.send_message(message.from_user.id, "Не удалось найти пользователя в БД",
                                       reply_markup=nav.admin_menu())
        case "delete":
            if db.client_exist(int(data["answer"])):
                if data["answer"].isdigit():
                    await bot.send_message(message.from_user.id, f"Пользователь {data['answer']} был удален из администраторов",
                                           reply_markup=nav.admin_menu())
                    db.update_data(int(data["answer"]), "role", "client")
                else:
                    if db.client_exist(data["answer"]):
                        await bot.send_message(message.from_user.id,
                                               f"Пользователь {data['answer']} был удален из администраторов",
                                               reply_markup=nav.admin_menu())
                        db.update_data(ID=data["answer"], place="username", data="role", value="client")
            else:
                await bot.send_message(message.from_user.id, "Не удалось найти пользователя в БД",
                                       reply_markup=nav.admin_menu())
    await state.finish()

def register_handlers_admin(dp: Dispatcher):
    dp.register_callback_query_handler(admin_menu, cb.filter(action=["admin_menu"]))
    dp.register_callback_query_handler(add_delete_admin, cb.filter(action=["delete_admin", "add_admin"]))
    dp.register_message_handler(action, state=getAnswer.answer)