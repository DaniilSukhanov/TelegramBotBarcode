import datetime

from aiogram import executor

import logging as lg

from aiogram.utils.exceptions import Unauthorized

from utils.misc import logging
from data import config
from loader import dp

import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.db_session import DataBase


async def on_startup(dispatcher):
    # Подключение к базе данных
    db = DataBase()

    # Обновление ошибок
    if config.CREATE_START_DATA:
        db.update_errors()

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    try:
        executor.start_polling(dp, on_startup=on_startup)
    except Unauthorized:
        lg.error('Invalid token.')
    except Exception as error:
        lg.error(f'Error: {error}.')
