from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.username}")
