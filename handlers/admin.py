from aiogram import types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt

from settings.config import bot, dp
from all_requests import request_api, request_db


# account
@dp.message_handler(commands=['profile'], state=None)
async def process_profile_command(msg: types.Message):
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
    await bot.send_message(msg.chat.id, text, parse_mode="HTML")
