from logging import basicConfig, INFO

from aiogram import executor
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from loader import dp, db

user_message = 'Пользователь'
admin_message = 'Админ'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(user_message, admin_message)

    await message.answer('''Привет, здесь мы подбираем самые ТОП-овые исходы из всей линии по индивидуальным заказам.

Работаем с 2017 года, а за 2023 было выполнено 14583 заказа. 


💳 Для покупки введи /menu
❓ Для связи со мной (Саша), введи /sos
    ''', reply_markup=markup)


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    cid = message.chat.id
    if cid not in ADMINS:
        ADMINS.append(cid)

    await message.answer('Включен админский режим.',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    cid = message.chat.id
    if cid in ADMINS:
        ADMINS.remove(cid)

    await message.answer('Включен пользовательский режим.',
                         reply_markup=ReplyKeyboardRemove())


async def on_startup():
    basicConfig(level=INFO)
    db.create_tables()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
