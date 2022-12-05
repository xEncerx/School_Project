from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.data import Database

db = Database("data.db")
# ___________________________________________________________________
admin_id = db.getAdmins()
token = "5529050317:AAH2wlyDHls3KF2mRfLHOuaBqwW3hIdSt7o"  # токен бота
# ___________________________________________________________________

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
