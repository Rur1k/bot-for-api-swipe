from aiogram import types

from load_all import bot, dp
from all_requests import request_db


@dp.message_handler(commands=['start'], state=None)
async def process_start_command(msg: types.Message):
    request_db.create_new_user(msg.from_user.id, msg.chat.id)
    await bot.send_message(msg.chat.id, 'Бот запустился, жду комманд.')