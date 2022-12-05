from aiogram import executor
from handlers.client import bot_info, start, daily_reward, back, profile, spend_money, leaderboard, active_task
from handlers.admin import admin, create_task
from bot_data import dp


async def on_startup(_):
    print("Bot Started")


start.register_handlers_start(dp)
bot_info.register_handlers_bot_info(dp)
daily_reward.register_handlers_daily_reward(dp)
back.register_handlers_back(dp)
profile.register_handlers_profile(dp)
spend_money.register_handlers_spend_money(dp)
leaderboard.register_handlers_leaderboard(dp)
active_task.register_handlers_active_task(dp)

admin.register_handlers_admin(dp)
create_task.register_handlers_create_task(dp)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)