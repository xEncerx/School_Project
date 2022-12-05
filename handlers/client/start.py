from aiogram import types, Dispatcher
import markups as nav
from bot_data import bot, db
from datetime import datetime

async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f"👋 Привет, {message.from_user.first_name}", reply_markup=nav.main_keyboard(message.from_user.id))
    db.add_client(message.from_user.id, "2000-01-01 01:01:01.330771", message.from_user.username)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])