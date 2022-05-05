import logging

from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from utils.db_api.db_session import DataBase
from utils.db_api import models
from utils import misc
from data import const, exceptions


db = DataBase()


class LoginChecker(BaseMiddleware):
    """Фильтрует сообщение, отправление пользователями,
    которые не обладают нужными правами."""
    @staticmethod
    async def on_process_message(message: types.Message, data: dict):
        handler = current_handler.get()
        if handler is None:
            return
        clearance_level_handler = getattr(
            handler, 'clearance_level', const.REGISTERED_USER
        )
        user_id = message.from_user.id
        user = await db.get_user(str(user_id))
        if user is None:
            user_status = const.UNREGISTERED_USER
        else:
            user_status = user.tgu_user_status
        if clearance_level_handler > user_status:
            raise exceptions.LowLevelPermission()

