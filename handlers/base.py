from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import auth as key_auth
from keyboards import base as key_base
from keyboards import admin as key_admin

from settings.config import bot, dp
from all_requests import request_db


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    request_db.create_new_user(msg.from_user.id, msg.chat.id)
    if request_db.is_auth(msg.from_user.id):
        await bot.send_message(msg.chat.id,
                               'Главное меню SWIPE',
                               reply_markup=key_admin.buttons_menu)
    else:
        await bot.send_message(msg.chat.id,
                               'Добрый день! Это бот для приложения "Swipe", авторизуйтесь или зарегистрируйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(lambda message: message.text == "Отмена/Назад", state="*")
async def process_start_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    if request_db.is_auth(msg.from_user.id):
        await bot.send_message(msg.chat.id,
                               'Главное меню SWIPE',
                               reply_markup=key_admin.buttons_menu)
    else:
        await bot.send_message(msg.chat.id,
                               'Добрый день! Это бот для приложения "Swipe", авторизуйтесь или зарегистрируйтесь',
                               reply_markup=key_auth.button_auth)
