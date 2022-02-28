import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from playhouse.sqliteq import SqliteQueueDatabase

from settings.config import TOKEN


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Подключение к БД
sqlite_db = SqliteQueueDatabase('bot.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})
