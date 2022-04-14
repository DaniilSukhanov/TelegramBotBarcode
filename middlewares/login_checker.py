import logging

from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from utils.db_api.db_session import DataBase
from utils.db_api import models
from utils import misc
from data import const


db = DataBase()


class LoginChecker(BaseMiddleware):
    @staticmethod
    async def on_process_message(message: types.Message, data: dict):
        handler = current_handler.get()
        if handler is None:
            return
        clearance_level_handler = getattr(
            handler, 'clearance_level', const.REGISTERED_USER
        )
        user_id = message.from_user.id
        user = db.get_user(str(user_id))
        prefix = ''
        if user is None:
            user_status = const.UNREGISTERED_USER
            prefix = '\nзарегистрируйтесь (/register).'
        else:
            user_status = user.tgu_user_status
        if clearance_level_handler > user_status:
            await message.answer('Вы не обладаете нужными правами.' + prefix)
            raise CancelHandler()

