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
async def login_email(msg: types.Message, state: FSMContext):
    email = msg.text
    await state.update_data(email=email)
    await bot.send_message(msg.chat.id, 'Введите пароль')
    await LoginState.next()


@dp.message_handler(state=LoginState.password)
async def login_password(msg: types.Message, state: FSMContext):
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
    await RegistrationStates.username.set()


@dp.message_handler(state=RegistrationStates.username)
async def register_username(msg: types.Message, state: FSMContext):
    username = msg.text
    await state.update_data(username=username)
    await bot.send_message(msg.chat.id, 'Укажите email')
    await RegistrationStates.email.set()


@dp.message_handler(state=RegistrationStates.email)
async def register_email(msg: types.Message, state: FSMContext):
    email = msg.text
    await state.update_data(email=email)
    await bot.send_message(msg.chat.id, 'Укажите пароль')
    await RegistrationStates.password.set()


@dp.message_handler(state=RegistrationStates.password)
async def register_password(msg: types.Message, state: FSMContext):
    password = msg.text
    await state.update_data(password=password)
    await bot.send_message(msg.chat.id, 'Повторите пароль')
    await RegistrationStates.repeat_password.set()


@dp.message_handler(state=RegistrationStates.repeat_password)
async def register_repeat_password(msg: types.Message, state: FSMContext):
    repeat_password = msg.text
    data = await state.get_data()
    password = data.get('password')
    if repeat_password == password:
        await state.update_data(repeat_password=repeat_password)
        await bot.send_message(msg.chat.id, 'Укажите номер телефона')
        await RegistrationStates.phone.set()
    else:
        await bot.send_message(msg.chat.id, 'Пароли не совпадают. Повторите ввод пароля.')
        await RegistrationStates.password.set()


@dp.message_handler(state=RegistrationStates.phone)
async def register_phone(msg: types.Message, state: FSMContext):
    phone = msg.text
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    reg = request_api.registration(username, email, password, phone)

    if reg:
        await bot.send_message(msg.chat.id, f'Регистрация прошла успешно, на почту {email} отправлено письмо с поддтверждение.')
    else:
        await bot.send_message(msg.chat.id, 'Регисрация не успешна, для повторной регистрации введите /registration')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
