import re

import aiogram.utils.markdown as fmt

from keyboards import auth as key_auth
from keyboards import base as key_base
from keyboards import admin as key_admin

from aiogram import types
from aiogram.dispatcher import FSMContext

from settings.config import bot, dp
from settings.states import LoginState, RegistrationStates
from all_requests import request_api, request_db


def validate_email(email):
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
    if re.match(pattern, email) is None:
        return False
    else:
        return True


def validate_password(password):
    regular = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

    pat = re.compile(regular)
    mat = re.search(pat, password)

    if mat:
        return True
    else:
        return False

def is_valid_phone(phone) -> bool:
    text = re.sub(r'\D', '', phone)
    return bool(re.search(r"^38\d{10}$", text))

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

    if validate_email(email) is False:
        await bot.send_message(msg.chat.id, 'Email - имеет не коррекный формат, введите email повторно.')
        await RegistrationStates.email.set()
    else:
        await state.update_data(email=email)
        text = fmt.text(
            fmt.text(fmt.hbold("Укажите пароль в формате:")),
            fmt.text(fmt.hbold('1. Должен содержать число.')),
            fmt.text(fmt.hbold('2. Должен содержать символ верхнего и нижнего регистра.')),
            fmt.text(fmt.hbold('3. Должен иметь хотя бы один специальный символ.')),
            fmt.text(fmt.hbold('4. Должно быть от 6 до 20 символов.')),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML")
        await RegistrationStates.password.set()


@dp.message_handler(state=RegistrationStates.password)
async def register_password(msg: types.Message, state: FSMContext):
    password = msg.text

    if validate_password(password):
        await state.update_data(password=password)
        await bot.send_message(msg.chat.id, 'Повторите пароль')
        await RegistrationStates.repeat_password.set()
    else:
        await bot.send_message(msg.chat.id, 'Пароль не соответсвует формату, повторите ввод.')
        await RegistrationStates.password.set()


@dp.message_handler(state=RegistrationStates.repeat_password)
async def register_repeat_password(msg: types.Message, state: FSMContext):
    repeat_password = msg.text
    data = await state.get_data()
    password = data.get('password')
    if repeat_password == password:
        await state.update_data(repeat_password=repeat_password)
        await bot.send_message(msg.chat.id, 'Укажите номер телефона в формате +380XXXXXXXXX')
        await RegistrationStates.phone.set()
    else:
        await bot.send_message(msg.chat.id, 'Пароли не совпадают. Повторите ввод пароля.')
        await RegistrationStates.password.set()


@dp.message_handler(state=RegistrationStates.phone)
async def register_phone(msg: types.Message, state: FSMContext):
    phone = msg.text
    await state.update_data(phone=phone)
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if is_valid_phone(phone):
        reg = request_api.registration(username, email, password, phone)

        if reg:
            await bot.send_message(msg.chat.id,
                                   f'Регистрация прошла успешно, на почту {email} отправлено письмо с поддтверждение.',
                                   reply_markup=key_auth.button_auth)
            await state.finish()
        else:
            await bot.send_message(msg.chat.id,
                                   'Регисрация не успешна, можно отменить регистрацию или '
                                   'изменить ранее ввведенные данные.',
                                   reply_markup=key_auth.button_edit_regdata)
            await RegistrationStates.wait_reg.set()
    else:
        await bot.send_message(msg.chat.id, 'Номер телефона не соответсвует формату, повторите ввод.')
        await RegistrationStates.phone.set()


@dp.message_handler(lambda message: message.text == "Изменить данные", state='*')
async def process_edit_registration_command(msg: types.Message, state: FSMContext):
    if not request_db.is_auth(msg.from_user.id):
        data = await state.get_data()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')

        text = fmt.text(
            fmt.text(fmt.hbold("***Скопируйте шаблон без этой строки***")),
            fmt.text(fmt.hbold('Имя пользователя: ', username)),
            fmt.text(fmt.hbold('Email: ', email)),
            fmt.text(fmt.hbold('Пароль: ', password)),
            fmt.text(fmt.hbold('Повторите пароль: ', password)),
            fmt.text(fmt.hbold('Номер телефона: ', phone)),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML")
        await RegistrationStates.edit_regdata.set()
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы авторизованы, сначала выйдите',
                               reply_markup=key_admin.buttons_menu)


@dp.message_handler(state=RegistrationStates.edit_regdata)
async def register_edit(msg: types.Message, state: FSMContext):
    new_regdata = msg.text
    new_regdata  = new_regdata.split('\n')
    data_for_save = []
    for data in new_regdata:
        data = data.split(':')
        data_for_save.append(data[1].strip())

    username = data_for_save[0]
    email = data_for_save[1]
    password = data_for_save[2]
    repeat_password = data_for_save[3]
    phone = data_for_save[4]

    if validate_email(email):
        if validate_password(password):
            if password==repeat_password:
                if is_valid_phone(phone):
                    reg = request_api.registration(username, email, password, phone)

                    if reg:
                        await bot.send_message(msg.chat.id,
                                               f'Регистрация прошла успешно, на почту {email} отправлено письмо с '
                                               f'поддтверждение.',
                                               reply_markup=key_auth.button_auth)
                        await state.finish()
                    else:
                        await bot.send_message(msg.chat.id,
                                               'Регисрация не успешна, можно отменить регистрацию или '
                                               'изменить ранее ввведенные данные.',
                                               reply_markup=key_auth.button_edit_regdata)
                else:
                    await bot.send_message(msg.chat.id,
                                           'Номер не подходит по формату, можно отменить регистрацию или '
                                           'изменить ранее ввведенные данные.',
                                           reply_markup=key_auth.button_edit_regdata)
            else:
                await bot.send_message(msg.chat.id,
                                       'Пароли не совпадают, можно отменить регистрацию или '
                                       'изменить ранее ввведенные данные.',
                                       reply_markup=key_auth.button_edit_regdata)
        else:
            await bot.send_message(msg.chat.id,
                                   'Пароль - введен не корректно, можно отменить регистрацию или '
                                   'изменить ранее ввведенные данные.',
                                   reply_markup=key_auth.button_edit_regdata)
    else:
        await bot.send_message(msg.chat.id,
                               'Email - введен не корректно, можно отменить регистрацию или '
                               'изменить ранее ввведенные данные.',
                               reply_markup=key_auth.button_edit_regdata)

