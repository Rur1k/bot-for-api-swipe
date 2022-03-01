import os
import sys
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from peewee import SqliteDatabase

from playhouse.sqliteq import SqliteQueueDatabase
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
API = os.getenv("API")
AUTH = os.getenv("AUTH")

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Подключение к БД
sqlite_db = SqliteDatabase('./bot.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})
