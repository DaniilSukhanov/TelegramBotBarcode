import logging

from aiogram import Dispatcher
from aiogram.utils.exceptions import ChatNotFound

from utils.db_api.db_session import DataBase


db = DataBase()


async def on_startup_notify(dp: Dispatcher):
    admins = await db.get_admins()
    for admin in admins:
        try:
            await dp.bot.send_message(admin.tgu_chat_id, "Бот Запущен")
        except ChatNotFound:
            logging.warning(
                f'Unable to find chat admin {admin.tgu_login}.'
            )
        except Exception as err:
            logging.exception(err)
