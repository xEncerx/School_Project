from aiogram import types, Dispatcher
import markups as nav
from bot_data import bot, db, admin_id
from markups import cb
from utils.message_utils import text_editor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from datetime import datetime

class getAnswer_task(StatesGroup):
    answer = State()


async def show_menu(call: types.CallbackQuery):
    await text_editor(text="Добро пожаловать в меню создания заданий:\n"
                           "Используйте клавиатуру ниже, чтобы создать задание", call=call, markup=nav.createTask_menu())

async def button_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action[:10] == "task_class":
        await text_editor(text=f"Ограничение установлено на {action[11:]} класс", call=call, markup=nav.createTask_menu())
        db.add_task_data("class", action[11:])
    match action:
        case "class_limit":
            await text_editor(text="Выберите ограничение по классам: ", call=call, markup=nav.createTask_class())
        case "time_limit":
            await text_editor(text="Введите дату окончания работы.\n<b>Вид: 02.12.2022 17:45</b>", call=call, markup=nav.back_button("cancle_data"))
            await getAnswer_task.answer.set()
            await state.update_data(type="time_limit")
        case "add_data":
            await text_editor(text="Пришлите мне текст/фотографию(+текст)/файл(+текст)/видео(+текст):",
                              call=call, markup=nav.back_button("cancle_data"))
            await getAnswer_task.answer.set()
            await state.update_data(type="data")
        case "add_limit":
            await text_editor(text="Выберите какое ограничение добавить:", call=call, markup=nav.limit_menu())
        case "preview":
            file_type = db.get_task_data("file_type")
            if file_type == "photo":
                await bot.send_photo(call.from_user.id, photo=db.get_task_data("file_id"), caption=db.get_task_data("text"))
            elif file_type == "document":
                await bot.send_document(call.from_user.id, document=db.get_task_data("file_id"), caption=db.get_task_data("text"))
            elif file_type == "video":
                await bot.send_video(call.from_user.id, video=db.get_task_data("file_id"), caption=db.get_task_data("text"))
            else:
                try:
                    await bot.send_message(call.from_user.id, db.get_task_data("text"))
                except: await bot.send_message(call.from_user.id, "NONE...")
            await bot.send_message(call.from_user.id, 'Задание будет выглядеть следующим образом 👆\n\n'
                                                      f'Ограничение установленно на "<b>{db.get_task_data("class")}</b>" класс\n'
                                                      f'Цена за выполнение: "<b>{db.get_task_data("price")}</b>"\n'
                                                      f'Выполнить до <b>"{db.get_task_data("end_time")}"</b>',
                                   reply_markup=nav.createTask_menu(), parse_mode=types.ParseMode.HTML)
        case "task_price":
            await text_editor(text="Введите цена за выполнение задания:", call=call)
            await getAnswer_task.answer.set()
            await state.update_data(type="price")

        case "publish_task":
            try:
                if db.get_task_data("price") is not None:
                    sent = 0
                    not_sent = 0
                    await text_editor(text='<b>✅ Рассылка успешно создана</b>', call=call)
                    match db.get_task_data("file_type"):
                        case None:
                            if db.get_task_data("text") is not None:
                                text = db.get_task_data("text")
                                price = db.get_task_data("price")
                                time = db.get_task_data("end_time")
                                for user in db.get_all_users(db.get_task_data("class")):
                                    try:
                                        await bot.send_message(chat_id=user[0],
                                                               text=f"{text}\n\nЦена за выполнение: {price} монет\n"
                                                                    f"Выполнить до {time if time is not None else 'неограниченно'}",
                                                               reply_markup=nav.accept_task(db.get_last_task()))
                                        sent += 1
                                    except:
                                        not_sent += 1
                                        continue
                        case "photo":
                            if db.get_task_data("text") is not None:
                                file_id = db.get_task_data("file_id")
                                text = db.get_task_data("text")
                                time = db.get_task_data("end_time")
                                price = db.get_task_data("price")
                                for user in db.get_all_users(db.get_task_data("class")):
                                    try:
                                        await bot.send_photo(chat_id=user[0], photo=file_id, caption=f"{text}\n\nЦена за выполнение: {price} монет\n"
                                                                                                     f"Выполнить до {time if time is not None else 'неограниченно'}",
                                                             reply_markup=nav.accept_task(db.get_last_task()))
                                        sent += 1
                                    except:
                                        not_sent += 1
                                        continue
                        case "document":
                            if db.get_task_data("text") is not None:
                                file_id = db.get_task_data("file_id")
                                text = db.get_task_data("text")
                                price = db.get_task_data("price")
                                time = db.get_task_data("end_time")
                                for user in db.get_all_users(db.get_task_data("class")):
                                    try:
                                        await bot.send_document(chat_id=user[0], document=file_id, caption=f"{text}\n\nЦена за выполнение: {price} монет\n"
                                                                                                           f"Выполнить до {time if time is not None else 'неограниченно'}",
                                                                reply_markup=nav.accept_task(db.get_last_task()))
                                        sent += 1
                                    except:
                                        not_sent += 1
                                        continue
                        case "video":
                            if db.get_task_data("text") is not None:
                                file_id = db.get_task_data("file_id")
                                text = db.get_task_data("text")
                                price = db.get_task_data("price")
                                time = db.get_task_data("end_time")
                                for user in db.get_all_users(db.get_task_data("class")):
                                    try:
                                        await bot.send_video(chat_id=user[0], video=file_id, caption=f"{text}\n\nЦена за выполнение: {price} монет\n"
                                                                                                     f"Выполнить до {time if time is not None else 'неограниченно'}",
                                                             reply_markup=nav.accept_task(db.get_last_task()))
                                        sent += 1
                                    except:
                                        not_sent += 1
                                        continue
                    await bot.send_message(call.from_user.id,
                                           f'<b>🛎 Статистика рассылки:\n\n🔔 - {sent}\n🔕 - {not_sent}</b>', parse_mode=types.ParseMode.HTML, reply_markup=nav.admin_menu())
                    db.add_task_data("status", "published")
                else:
                    await call.answer("Установите цену за выполнение задания", show_alert=True)
            except:
                await call.answer("Установить данные!", show_alert=True)
    await call.answer()

async def update_data(message: types.Message, state: FSMContext):
    b = await state.get_data()
    if b["type"] == "data":
        if message.content_type == "text":
            async with state.proxy() as data:
                data["answer"] = message.text
            db.add_task_data("text", data["answer"])
        if message.content_type == "photo":
            async with state.proxy() as data:
                data["photo_id"] = message.photo[-1].file_id
                if message.caption is not None:
                    data["caption"] = message.caption
                    db.add_task_data("text", data["caption"])
                db.add_task_data("file_id", data["photo_id"])
                db.add_task_data("file_type", "photo")
        if message.content_type == "document":
            async with state.proxy() as data:
                data["doc_id"] = message.document.file_id
                if message.caption is not None:
                    data["caption"] = message.caption
                    db.add_task_data("text", data["caption"])
            db.add_task_data("file_id", data["doc_id"])
            db.add_task_data("file_type", "document")
        if message.content_type == "video":
            async with state.proxy() as data:
                data["video_id"] = message.video.file_id
                if message.caption is not None:
                    data["caption"] = message.caption
                    db.add_task_data("text", data["caption"])
            db.add_task_data("file_id", data["video_id"])
            db.add_task_data("file_type", "video")
        await bot.send_message(message.from_user.id, "Данные успешно сохранены", reply_markup=nav.createTask_menu())
    if b["type"] == "price":
        async with state.proxy() as data:
            data["price"] = message.text
        if data["price"].isdigit():
            await bot.send_message(message.from_user.id, "Цена была успешно установлена", reply_markup=nav.createTask_menu())
            db.add_task_data("price", data["price"])
        else:
            await bot.send_message(message.from_user.id, "<b>Цена должна быть числом!</b>", reply_markup=nav.createTask_menu(), parse_mode=types.ParseMode.HTML)
    if b["type"] == "time_limit":
        async with state.proxy() as data:
            data["time"] = message.text
        try:
            time = datetime.strptime(data["time"], '%d.%m.%Y %H:%M')
            db.add_task_data("end_time", time)
            await bot.send_message(message.from_user.id, f"Даты была успешно обновлена: <b>{time}</b>",
                                   parse_mode=types.ParseMode.HTML, reply_markup=nav.createTask_menu())
            await state.finish()
        except:
            await bot.send_message(message.from_user.id, "Произошла ошибка в определение времени.\n"
                                                         "Проверьте правильность написания и заполните дату ещё раз", reply_markup=nav.createTask_menu())
    await state.finish()


def register_handlers_create_task(dp: Dispatcher):
    dp.register_callback_query_handler(show_menu, cb.filter(action=["create_task"]))
    dp.register_callback_query_handler(button_handler, cb.filter(action=["publish_task", "preview", "add_limit", "add_data", "task_class_1", "task_class_2", "task_class_3",
                                                                         "task_class_4", "task_class_5", "task_class_6", "task_class_7", "task_class_8",
                                                                         "task_class_9", "task_class_10", "task_class_11", "task_price", "class_limit", "time_limit"]))
    dp.register_message_handler(update_data, state=getAnswer_task.answer, content_types=types.ContentTypes.ANY)