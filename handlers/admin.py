from aiogram import types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt

from settings.config import bot, dp
from settings.states import AccountState
from all_requests import request_api, request_db

from keyboards import auth as key_auth
from keyboards import base as key_base
from keyboards import admin as key_admin


# account
@dp.message_handler(lambda message: message.text == "Профиль", state="*")
async def process_profile_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        data = request_api.account_detail(token)
        text = fmt.text(
                    fmt.text(fmt.hbold("Имя пользователя: "), data['username']),
                    fmt.text(fmt.hbold("Email: "), data['email']),
                    fmt.text(fmt.hbold("Телефон: "), data['phone']),
                    fmt.text(fmt.hbold("Имя: "), data['first_name']),
                    fmt.text(fmt.hbold("Фамилия: "), data['last_name']),
                    fmt.text(fmt.hbold("Роль: "), data['role']),
                    sep="\n"
            )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=key_admin.buttons_account)
        await AccountState.switch.set()
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(state=AccountState.switch)
async def account_switch(msg: types.Message, state: FSMContext):
    choice = msg.text
    if choice == 'Изменить номер телефона':
        await bot.send_message(msg.chat.id, 'Введите новый номер телефона', reply_markup=key_admin.button_account_cancel)
        await AccountState.phone.set()
    elif choice == 'Изменить имя':
        await bot.send_message(msg.chat.id, 'Введите имя', reply_markup=key_admin.button_account_cancel)
        await AccountState.first_name.set()
    elif choice == 'Изменить фамилию':
        await bot.send_message(msg.chat.id, 'Введите фамилию', reply_markup=key_admin.button_account_cancel)
        await AccountState.last_name.set()
    else:
        await bot.send_message(msg.chat.id, 'Я не знаю такой команды, попробуйте еще раз!')
        await AccountState.switch.set()


@dp.message_handler(state=AccountState.phone)
async def account_phone(msg: types.Message, state: FSMContext):
    phone = msg.text
    token = request_db.get_token_user(msg.from_user.id)
    save_data = request_api.account_update(token, phone=phone)
    await state.reset_state()
    if save_data:
        await bot.send_message(msg.chat.id, 'Новый номер указан.',
                               reply_markup=key_admin.button_account_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_account_cancel)


@dp.message_handler(state=AccountState.first_name)
async def account_first_name(msg: types.Message, state: FSMContext):
    first_name = msg.text
    token = request_db.get_token_user(msg.from_user.id)
    save_data = request_api.account_update(token, first_name=first_name)
    await state.reset_state()
    if save_data:
        await bot.send_message(msg.chat.id, 'Новое имя указано.',
                               reply_markup=key_admin.button_account_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_account_cancel)


@dp.message_handler(state=AccountState.last_name)
async def account_last_name(msg: types.Message, state: FSMContext):
    last_name = msg.text
    token = request_db.get_token_user(msg.from_user.id)
    save_data = request_api.account_update(token, last_name=last_name)
    await state.reset_state()
    if save_data:
        await bot.send_message(msg.chat.id, 'Новая фамилия указана.',
                               reply_markup=key_admin.button_account_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_account_cancel)


# announcement
@dp.message_handler(lambda message: message.text == "Объявления", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в Объявления', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(lambda message: message.text == "Дома", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в Дома', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(lambda message: message.text == "Квартиры", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в Квартиры', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(lambda message: message.text == "Нотариусы", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в Нотариусы', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(lambda message: message.text == "Пользователи", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в пользователей', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(lambda message: message.text == "Избранное", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в избранное', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)

