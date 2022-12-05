from aiogram import types, Dispatcher
import markups as nav
from markups import cb
from bot_data import db, bot
from utils.message_utils import text_editor
from datetime import datetime

async def active_task(call: types.CallbackQuery):
    await text_editor(text="<b>COMING SOON...</b>",
                      call=call,
                      markup=nav.active_task_menu(db.get_client_data(call.from_user.id)[6]))

async def accept(call: types.CallbackQuery):
    db_time = datetime.strptime(db.get_task_data("end_time", call.data[7:]), "%Y-%m-%d %H:%M:%S")
    if len(db.get_client_data(call.from_user.id)[6]) < 1 and datetime.now() <= db_time:
        action = call.data[7:]
        db.update_data(call.from_user.id, "active_task", action)
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(call.from_user.id, f"Вы успешно взяли задание с ID: <b>{action}</b> в работу", parse_mode=types.ParseMode.HTML, reply_markup=nav.back_button("main_menu"))
        except:
            await text_editor(text=f"Вы успешно взяли задание с ID: <b>{action}</b> в работу",
                              call=call, markup=nav.back_button("main_menu"))
    elif len(db.get_client_data(call.from_user.id)[6]) >= 1:
        await call.answer("В работу можно взять только 1 задание!", show_alert=True)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    elif datetime.now() > db_time:
        await call.answer("Время выполнения задания истекло", show_alert=True)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.answer()

async def reject(call: types.CallbackQuery):
    await text_editor(text=f"👋 Привет, {call.from_user.first_name}",
                      call=call,
                      markup=nav.main_keyboard(call.from_user.id))
    await call.answer()

async def enter_task_menu(call: types.CallbackQuery):
    action = call.data[8:]
    file_id = db.get_task_data("file_id", action)
    text = db.get_task_data("text", action)
    time = db.get_task_data("end_time", action)
    price = db.get_task_data("price", action)
    match db.get_task_data("file_type", action):
        case None:
            if db.get_task_data("text") is not None:
                await bot.send_message(chat_id=call.from_user.id,
                                       text=f"{text}\n\nЦена за выполнение: {price} монет\n"
                                            f"Выполнить до {time}",
                                       reply_markup=nav.back_button("main_menu"))
        case "photo":
            if db.get_task_data("text") is not None:
                await bot.send_photo(chat_id=call.from_user.id, photo=file_id,
                                     caption=f"{text}\n\nЦена за выполнение: {price} монет\n"
                                             f"Выполнить до {time}",
                                     reply_markup=nav.back_button("main_menu"))
        case "document":
            if db.get_task_data("text") is not None:
                await bot.send_document(chat_id=call.from_user.id, document=file_id,
                                        caption=f"{text}\n\nЦена за выполнение: {price} монет\n"
                                                f"Выполнить до {time}",
                                        reply_markup=nav.back_button("main_menu"))
        case "video":
            if db.get_task_data("text") is not None:
                await bot.send_video(chat_id=call.from_user.id, video=file_id,
                                     caption=f"{text}\n\nЦена за выполнение: {price} монет\n"
                                             f"Выполнить до {time}",
                                     reply_markup=nav.back_button("main_menu"))
    await call.answer()

def register_handlers_active_task(dp: Dispatcher):
    dp.register_callback_query_handler(active_task, cb.filter(action="active_tasks"))
    dp.register_callback_query_handler(accept, text_contains="accept")
    dp.register_callback_query_handler(reject, text="reject")
    dp.register_callback_query_handler(enter_task_menu, text_contains="task_id")