import request_api

from aiogram import types
from aiogram import executor
from aiogram.dispatcher import FSMContext

from load_all import bot, dp
from states import LoginState, RegistrationStates
from request_db import *


@dp.message_handler(commands=['start'], state=None)
async def process_start_command(msg: types.Message):
    create_new_user(msg.from_user.id, msg.chat.id)
    await bot.send_message(msg.chat.id, 'Бот запустился, жду комманд.')


# login


@dp.message_handler(commands=['login'], state=None)
async def process_login_command(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Введите email')
    await LoginState.email.set()


@dp.message_handler(state=LoginState.email)
async def write_email(msg: types.Message, state: FSMContext):
    email = msg.text
    await state.update_data(email=email)
    await bot.send_message(msg.chat.id, 'Введите пароль')
    await LoginState.next()


@dp.message_handler(state=LoginState.password)
async def write_password(msg: types.Message, state: FSMContext):
    password = msg.text
    data = await state.get_data()
    email = data.get('email')
    code, value = request_api.login(email, password)

    if code == 'ERROR':
        await bot.send_message(msg.chat.id, value+". Введите /login для повторной попытке авторизации")
    elif code == 'SUCCESS':
        await bot.send_message(msg.chat.id, "Авторизация прошла успешно.")
        set_token_user(msg.from_user.id, value)
    await state.finish()


# registration

@dp.message_handler(commands=['registration'], state=None)
async def process_registration_command(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Укажите имя пользователя')
    await LoginState.email.set()


@dp.message_handler(state=LoginState.email)
async def write_email(msg: types.Message, state: FSMContext):
    email = msg.text
    await state.update_data(email=email)
    await bot.send_message(msg.chat.id, 'Введите пароль')
    await LoginState.next()


@dp.message_handler(state=LoginState.password)
async def write_password(msg: types.Message, state: FSMContext):
    password = msg.text
    data = await state.get_data()
    email = data.get('email')
    code, value = request_api.login(email, password)

    if code == 'ERROR':
        await bot.send_message(msg.chat.id, value+". Введите /login для повторной попытке авторизации")
    elif code == 'SUCCESS':
        await bot.send_message(msg.chat.id, "Авторизация прошла успешно.")
        set_token_user(msg.from_user.id, value)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
