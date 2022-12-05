from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from bot_data import db

cb = CallbackData("fabnum", "action")


def main_keyboard(user_id: int = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🏆 Таблица лидеров", callback_data=cb.new(action="leaderboard")),
        InlineKeyboardButton("📥 Активные задания", callback_data=cb.new(action="active_tasks")),
        InlineKeyboardButton("🛒 Потратить монеты", callback_data=cb.new(action="spend_money")))
    keyboard.row(InlineKeyboardButton("💾 Профиль", callback_data=cb.new(action="profile")),
                 InlineKeyboardButton("⚙ Информация о боте", callback_data=cb.new(action="bot_info")))
    keyboard.add(InlineKeyboardButton("🎁 Ежедневная награда", callback_data=cb.new(action="daily_reward")))
    if user_id in db.getAdmins():
        keyboard.add(InlineKeyboardButton("admin_menu", callback_data=cb.new(action="admin_menu")))
    return keyboard

get_dailyreward_button = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("🎉 Получить", callback_data=cb.new(action="get_dailyreward")),
                                                               InlineKeyboardButton("🔙 Назад", callback_data="back|main_menu"))

def back_button(data: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data=f"back|{data}"))
    return keyboard

def profile_keyboard1():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("📥 Выбрать класс обучения", callback_data=cb.new(action="choose_class")),
                 InlineKeyboardButton("🔙 Назад", callback_data=f"back|main_menu"))
    return keyboard

def profile_keyboard2():
    keyboard = InlineKeyboardMarkup(row_width=6)
    for i in range(1, 12):
        keyboard.insert(InlineKeyboardButton(f"{i}", callback_data=cb.new(action=f"class_{i}")))
    keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data=f"back|profile_menu"))
    return keyboard

def show_shop_list(array: list):
    keyboard = InlineKeyboardMarkup()
    for i in array:
        keyboard.add(InlineKeyboardButton(f"{i[0]} - {i[1]} руб", callback_data=f"{i[0]}"))
    keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data=f"back|main_menu"))
    return keyboard

def admin_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(InlineKeyboardButton("Добавить Админа", callback_data=cb.new(action=f"add_admin")),
                 InlineKeyboardButton("Удалить Админа", callback_data=cb.new(action=f"delete_admin")))
    keyboard.add(InlineKeyboardButton("Создать задание", callback_data=cb.new(action=f"create_task")))
    keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data=f"back|main_menu"))
    return keyboard

def createTask_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("🖋 Добавить текст", callback_data=cb.new(action=f"add_data")),
                 InlineKeyboardButton("🔒 Добавить ограничения", callback_data=cb.new(action=f"add_limit")))
    keyboard.add(InlineKeyboardButton("💵 Цена за выполнение", callback_data=cb.new(action=f"task_price")))
    keyboard.add(InlineKeyboardButton("🔍 Предпросмотр", callback_data=cb.new(action=f"preview")),
                 InlineKeyboardButton("📤 Опубликовать задание", callback_data=cb.new(action=f"publish_task")),
                 InlineKeyboardButton("🔙 Назад", callback_data=f"back|cancle_create_task"))
    return keyboard

def createTask_class():
    keyboard = InlineKeyboardMarkup(row_width=6)
    for i in range(1, 12):
        keyboard.insert(InlineKeyboardButton(f"{i}", callback_data=cb.new(action=f"task_class_{i}")))
    keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data=f"back|create_task_menu"))
    return keyboard

def accept_task(id: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("✅ Принять", callback_data=f"accept|{id}"),
                 InlineKeyboardButton("❌ Отклонить", callback_data=f"reject"),
                 InlineKeyboardButton("📌 Главное меню", callback_data="back|main_menu"))
    return keyboard

def active_task_menu(task_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if task_id:
        keyboard.add(
            InlineKeyboardButton(f"📃 Задание {task_id}", callback_data=f"task_id|{task_id}"),
            InlineKeyboardButton("🔙 Назад", callback_data=f"back|main_menu"))
    else:
        keyboard.add(InlineKeyboardButton("❌ У вас нету заданий", callback_data="???"),
                     InlineKeyboardButton("🔙 Назад", callback_data=f"back|main_menu"))
    return keyboard

def limit_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("🗄 Классы", callback_data=cb.new(action="class_limit")),
                 InlineKeyboardButton("⏱ Время", callback_data=cb.new(action="time_limit")),
                 InlineKeyboardButton("🔙 Назад", callback_data=f"back|create_task_menu"))
    return keyboard