from keyboards import auth as key_auth
from keyboards import base as key_base
from keyboards import admin as key_admin

from aiogram import types
from aiogram.dispatcher import FSMContext

from settings.config import bot, dp
from settings.states import LoginState, RegistrationStates
from all_requests import request_api, request_db


# login

@dp.message_handler(lambda message: message.text == "Выход")
async def process_logout_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        state_logout = request_api.logout(token)
        if state_logout:
            request_db.set_token_user(msg.from_user.id, None, True)
            await bot.send_message(msg.chat.id, 'Вы успешно вылогинились!', reply_markup=key_auth.button_auth)
        else:
            await bot.send_message(msg.chat.id,
                                   'Упс, что-то произошло не так свяжитесь с разработчиком!',
                                   reply_markup=key_admin.buttons_menu)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(lambda message: message.text == "Вход", state=None)
async def process_login_command(msg: types.Message):
    if not request_db.is_auth(msg.from_user.id):
        await bot.send_message(msg.chat.id, 'Введите email', reply_markup=key_base.button_cancel)
        await LoginState.email.set()
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы авторизованы, сначала выйдите',
                               reply_markup=key_admin.buttons_menu)


@dp.message_handler(state=LoginState.email)
async def login_email(msg: types.Message, state: FSMContext):
    email = msg.text
    await state.update_data(email=email)
    await bot.send_message(msg.chat.id, 'Введите пароль', reply_markup=key_base.button_cancel)
    await LoginState.next()


@dp.message_handler(state=LoginState.password)
async def login_password(msg: types.Message, state: FSMContext):
    password = msg.text
    data = await state.get_data()
    email = data.get('email')
    code, value = request_api.login(email, password)

    if code == 'ERROR':
        await bot.send_message(msg.chat.id,
                               value+'. Нажмите "Вход" для повторной попытки авторизации',
                               reply_markup=key_auth.button_auth)
    elif code == 'SUCCESS':
        await bot.send_message(msg.chat.id, "Авторизация прошла успешно.", reply_markup=key_admin.buttons_menu)
        request_db.set_token_user(msg.from_user.id, value)
    await state.finish()


# registration

@dp.message_handler(lambda message: message.text == "Регистрация", state=None)
async def process_registration_command(msg: types.Message):
    if not request_db.is_auth(msg.from_user.id):
        await bot.send_message(msg.chat.id, 'Укажите имя пользователя', reply_markup=key_base.button_cancel)
        await RegistrationStates.username.set()
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы авторизованы, сначала выйдите',
                               reply_markup=key_admin.buttons_menu)


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
        await bot.send_message(msg.chat.id,
                               f'Регистрация прошла успешно, на почту {email} отправлено письмо с поддтверждение.',
                               reply_markup=key_auth.button_auth)
    else:
        await bot.send_message(msg.chat.id,
                               'Регисрация не успешна, для повторной регистрации нажмите "Регистрация"',
                               reply_markup=key_auth.button_auth)
    await state.finish()
