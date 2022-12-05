from aiogram import types, Dispatcher
import markups as nav
from markups import cb
from bot_data import db
import random, string
from utils.message_utils import text_editor

async def shop(call: types.CallbackQuery):
    await text_editor(text="<b>Выберите на что хотите потратить монеты:</b>", call=call, markup=nav.show_shop_list(db.get_shop_list()))
    await call.answer()


async def buy_product(call: types.CallbackQuery):
    name = call.data
    if db.get_client_data(call.from_user.id)[1] >= db.get_product_price(name):
        await text_editor(text=f"Вы купили <b>{name}</b> за <b>{db.get_product_price(name)} руб</b>\n\n"
                               f"Ваш купон: <b>{''.join(random.choices(string.digits+string.ascii_letters, k=random.randint(12, 18)))}</b>\n"
                               f"Обязательно сохраните купон, чтобы не потерять",
                          call=call,
                          markup=nav.back_button("shop_menu"))
        db.update_data(call.from_user.id, "balance", int(db.get_client_data(call.from_user.id)[1])-int(db.get_product_price(name)))
    else:
        await call.answer("⚠ У вас недостаточно средств")

def register_handlers_spend_money(dp: Dispatcher):
    dp.register_callback_query_handler(shop, cb.filter(action=["spend_money"]))
    dp.register_callback_query_handler(buy_product, lambda call: call.data in list(i[0] for i in db.get_shop_list()))