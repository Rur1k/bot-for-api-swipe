from aiogram import types
from aiogram.dispatcher import FSMContext

from settings.config import bot, dp
from all_requests import request_db
from keyboards import auth


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    request_db.create_new_user(msg.from_user.id, msg.chat.id)
    await bot.send_message(msg.chat.id,
                           'Добрый день! Это бот для приложения "Swipe", авторизуйтесь или зарегистрируйтесь',
                           reply_markup=auth.button_auth)


@dp.message_handler(lambda message: message.text == "Отмена", state="*")
async def process_start_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    await bot.send_message(msg.chat.id,
                           'Вы отменили состояние!',
                           reply_markup=None)

