from aiogram import types, Dispatcher
import markups as nav
from markups import cb
from bot_data import bot, db
from datetime import datetime, timedelta
import random
from utils.message_utils import text_editor

async def get_reward(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "daily_reward":
        await text_editor(call=call, text="🎁 Раз в день вы можете получить немного бесплатных монет\n"
                                          "📌 Получить можно от 1 до 5 монет", markup=nav.get_dailyreward_button)
    if action == "get_dailyreward":
        time = datetime.strptime(db.get_client_data(call.from_user.id)[3], '%Y-%m-%d %H:%M:%S.%f') + timedelta(days=1)
        if time <= datetime.now():
            reward = random.randint(1, 5)
            await text_editor(call=call, text=f"🎉 Поздравляю вы получили {reward}монет", markup=nav.back_button("main_menu"))
            db.update_data(call.from_user.id, "last_reward", datetime.now())
            db.update_data(call.from_user.id, "balance", db.get_client_data(call.from_user.id)[1] + reward)
        else:
            await call.answer("❗ Получить ежедневную награду можно только через 24 часа", show_alert=True)
    await call.answer()

def register_handlers_daily_reward(dp: Dispatcher):
    dp.register_callback_query_handler(get_reward, cb.filter(action=["daily_reward", "get_dailyreward"]))