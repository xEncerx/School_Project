from aiogram import types, Dispatcher
import markups as nav
from markups import cb
from bot_data import db, bot
from utils.message_utils import text_editor

async def leaderboard(call: types.CallbackQuery):
    text = ""
    array = sorted(db.get_leaderboard_data(db.get_client_data(call.from_user.id)[4]), key=lambda student: student[2])[::-1]
    for i in range(10):
        try:
            text += f"{i+1}){array[i][0]} - {array[i][2]}\n"
        except:
            text += f"{i+1}) ------"

    await text_editor(text="<b>Таблица лидеров</b>:\n\n"
                           f"Таблица лидеров показывает учеников <b>{db.get_client_data(call.from_user.id)[4]} класса</b>\n"
                           "Получай хорошие оценки и попадай сюда, чтобы получить монеты\n\n"
                           "Таблица обновляется раз в неделю\n"
                           "<b>Призы получают учащиеся с 1-10 место</b>\n\n"
                           f"<b>{text}</b>", call=call, markup=nav.back_button("main_menu"))

def register_handlers_leaderboard(dp: Dispatcher):
    dp.register_callback_query_handler(leaderboard, cb.filter(action="leaderboard"))

