import keyboard
import datetime

from aiogram import types
from aiogram import executor
from load_all import bot, dp
from request_api import *


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    pass
