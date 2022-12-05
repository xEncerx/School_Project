from aiogram import types, Dispatcher
import markups as nav
from markups import cb
from bot_data import db
from utils.message_utils import text_editor

async def profile(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    match action:
        case "profile":
            await text_editor(text="Профиль:\n"
                                   "➖➖➖➖➖➖➖➖➖\n"
                                   f"🔖 Имя: <b>{call.from_user.first_name}</b>\n"
                                   f"🔖 Username: @{call.from_user.username}\n"
                                   f"🆔 ID: <code>{call.from_user.id}</code>\n"
                                   f"📃 Класс обучения: <b>{'Выберите свой класс обучения' if db.get_client_data(call.from_user.id)[4] == '' else db.get_client_data(call.from_user.id)[4]}</b>\n"
                                   f"💰Balance: <b>{db.get_client_data(call.from_user.id)[1]}</b>\n"
                                   f"📊 Выполнено заданий: <b>{len(db.get_client_data(call.from_user.id)[5])}</b>\n"
                                   f"📈 Активных заданий: <b>{len(db.get_client_data(call.from_user.id)[6])}</b>\n"
                                   "➖➖➖➖➖➖➖➖➖",
                              call=call,
                              markup=nav.profile_keyboard1())
        case "choose_class":
            await text_editor(text="<b>Выберите класс обучения:</b>", call=call, markup=nav.profile_keyboard2())

async def get_class(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"][6:]
    db.update_data(call.from_user.id, "class", action)
    await text_editor(text="Профиль:\n"
                           "➖➖➖➖➖➖➖➖➖\n"
                           f"🔖 Имя: <b>{call.from_user.first_name}</b>\n"
                           f"🔖 Username: @{call.from_user.username}\n"
                           f"🆔 ID: <code>{call.from_user.id}</code>\n"
                           f"📃 Класс обучения: <b>{'Выберите свой класс обучения' if db.get_client_data(call.from_user.id)[4] == '' else db.get_client_data(call.from_user.id)[4]}</b>\n"
                           f"💰Balance: <b>{db.get_client_data(call.from_user.id)[1]}</b>\n"
                           f"📊 Выполнено заданий: <b>{len(db.get_client_data(call.from_user.id)[5])}</b>\n"
                           f"📈 Активных заданий: <b>{len(db.get_client_data(call.from_user.id)[6])}</b>\n"
                           "➖➖➖➖➖➖➖➖➖",
                      call=call,
                      markup=nav.profile_keyboard1())
    await call.answer()

def register_handlers_profile(dp: Dispatcher):
    dp.register_callback_query_handler(profile, cb.filter(action=["profile", "choose_class"]))
    dp.register_callback_query_handler(get_class, cb.filter(action=["class_1", "class_2", "class_3", "class_4", "class_5",
                                                                    "class_6", "class_7", "class_8", "class_9", "class_10", "class_11"]))