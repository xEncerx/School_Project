from aiogram import types, Dispatcher
import markups as nav
from markups import cb
from utils.message_utils import text_editor


async def get_info(call: types.CallbackQuery):
    await text_editor(text="➖ Автор: Мелихов Даниил\n"
                           "➖ Версия: 0.2\n"
                           "➖ Библиотеки: aiogram, sqlite3\n"
                           "➖In the future it will be removed➖",
                      call=call, markup=nav.back_button("main_menu"))
    await call.answer()


def register_handlers_bot_info(dp: Dispatcher):
    dp.register_callback_query_handler(get_info, cb.filter(action=["bot_info"]))