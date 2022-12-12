from aiogram import types
from bot_data import bot

async def text_editor(text: str, call: types.CallbackQuery, markup=None):
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode=types.ParseMode.HTML)
    except:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode=types.ParseMode.HTML)
        except: await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode=types.ParseMode.HTML)