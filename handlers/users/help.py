from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from data import const
from utils.misc.middleware_status_setters import clearance_level


@clearance_level(const.UNREGISTERED_USER)
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    
    await message.answer("\n".join(text))
