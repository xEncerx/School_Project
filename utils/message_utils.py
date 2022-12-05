from aiogram import types
from bot_data import bot

async def text_editor(text: str, call: types.CallbackQuery = None, message: types.Message = None, markup=None, is_call=True):
    if is_call:
        try:
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode=types.ParseMode.HTML)
        except:
            await bot.send_message(call.from_user.id, text, reply_markup=markup, parse_mode=types.ParseMode.HTML)
    else:
        try:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message_id, text=text, reply_markup=markup, parse_mode=types.ParseMode.HTML)
        except:
            await bot.send_message(message.from_user.id, text, reply_markup=markup, parse_mode=types.ParseMode.HTML)