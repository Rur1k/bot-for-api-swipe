from aiogram import types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt

from settings.config import bot, dp
from all_requests import request_api, request_db

from keyboards import auth as key_auth
from keyboards import base as key_base
from keyboards import admin as key_admin


# account
@dp.message_handler(lambda message: message.text == "Профиль", state=None)
async def process_profile_command(msg: types.Message):
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
        await bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


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

