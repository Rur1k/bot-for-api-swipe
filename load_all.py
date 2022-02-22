import asyncio
import logging

from peewee import SqliteDatabase
from config import TOKEN
from aiogram import Bot, Dispatcher

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Подключние к БД
sqlite_db = SqliteDatabase('/', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024*64})
