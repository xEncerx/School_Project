from aiogram import types, Dispatcher
import markups as nav
from markups import cb
from bot_data import db
from utils.message_utils import text_editor
from aiogram.dispatcher import FSMContext

async def back(call: types.CallbackQuery, state: FSMContext):
    action = call.data[5:]
    match action:
        case "main_menu":
            await text_editor(call=call, text="📍 Главное меню", markup=nav.main_keyboard(call.from_user.id))
        case "profile_menu":
            await text_editor(text="Профиль:\n"
                                   "➖➖➖➖➖➖➖➖➖\n"
                                   f"🔖 Имя: <b>{call.from_user.first_name}</b>\n"
                                   f"🔖 Username: @{call.from_user.username}\n"
                                   f"🆔 ID: <b>{call.from_user.id}</b>\n"
                                   f"📃 Класс обучения: <b>{'Выберите свой класс обучения' if db.get_client_data(call.from_user.id)[4] == '' else db.get_client_data(call.from_user.id)[4]}</b>\n"
                                   f"💰Balance: <b>{db.get_client_data(call.from_user.id)[1]}</b>\n"
                                   f"📊 Выполнено заданий: <b>0</b>\n"
                                   f"📈 Активных заданий: <b>0</b>\n"
                                   "➖➖➖➖➖➖➖➖➖",
                              call=call,
                              markup=nav.profile_keyboard1())
        case "shop_menu":
            await text_editor(text="<b>Выберите на что хотите потратить монеты:</b>", call=call,
                              markup=nav.show_shop_list(db.get_shop_list()))

        case "admin_menu":
            await text_editor(text="Добро пожаловать в Админ Меню:", call=call, markup=nav.admin_menu())

        case "cancle_create_task":
            if await state.get_state() is not None:
                await state.finish()
            db.delete_task()
            await text_editor(text="Добро пожаловать в Админ Меню:", call=call, markup=nav.admin_menu())

        case "create_task_menu":
            await text_editor(text="Добро пожаловать в меню создания заданий:\n"
                                   "Используйте клавиатуру ниже, чтобы создать задание", call=call,
                              markup=nav.createTask_menu())
        case "cancle_data":
            if await state.get_state() is not None:
                await state.finish()
            await text_editor(text="Добро пожаловать в меню создания заданий:\n"
                                   "Используйте клавиатуру ниже, чтобы создать задание", call=call,
                              markup=nav.createTask_menu())
    await call.answer()

def register_handlers_back(dp: Dispatcher):
    dp.register_callback_query_handler(back, text_contains="back", state="*")