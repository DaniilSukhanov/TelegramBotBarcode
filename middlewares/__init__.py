from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .login_checker import LoginChecker


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LoginChecker())
