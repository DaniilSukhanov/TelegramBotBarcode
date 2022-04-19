import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.db_session import DataBase

db = DataBase()
token = db.get_token(config.BOT_LOGIN)
bot = Bot(
    token=token, parse_mode=types.ParseMode.HTML
)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
