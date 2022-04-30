from aiogram import executor


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
    executor.start_polling(dp, on_startup=on_startup)

