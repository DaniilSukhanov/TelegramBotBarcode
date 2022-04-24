from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    phone_number = State()
    password = State()
