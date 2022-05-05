from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from data import const
from loader import dp
from utils.db_api import models
from utils.db_api.db_session import DataBase
from utils.misc import clearance_level, rate_limit


db = DataBase()


@clearance_level(const.ADMIN)
@dp.message_handler(Command('statistics'))
async def get_statistics(message: types.Message):
    count_new_users = await db.get_new_users()
    await message.answer(
        f'Количество новых пользователей за сегодня: {count_new_users}'
    )
