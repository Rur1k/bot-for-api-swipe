from aiogram import executor

from settings.config import dp

import handlers.base
import handlers.auth
import handlers.admin


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
