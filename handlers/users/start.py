from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data import const
from loader import dp, bot
from utils.misc import clearance_level


@clearance_level(const.UNREGISTERED_USER)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.username}. "
        f"Я бот, который может сканировать штрих-коды!"
    )
