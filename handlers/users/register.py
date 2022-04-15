import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from loader import dp, bot
from states import Register
from utils.db_api.db_session import DataBase
from utils.db_api import models
from keyboards.default import keyboard_getter_contact
from data import const
from utils.misc.middleware_status_setters import clearance_level


db = DataBase()


@clearance_level(const.UNREGISTERED_USER)
@dp.message_handler(Command('register'))
async def register(message: types.Message):
    """Ввод пользователя в состояние регистрации."""
    user = db.get_user(message.from_user.id)
    if user is None:
        await message.answer(
            'Началась регистрация.\n'
            'Поделитесь своим номером телефона с ботом.',
            reply_markup=keyboard_getter_contact
        )
        await Register.phone_number.set()
    else:
        await message.answer('Вы уже зарегистрировались.')


@clearance_level(const.UNREGISTERED_USER)
@dp.message_handler(
    state=Register.phone_number, content_types=types.ContentType.CONTACT
)
async def get_phone_number(message: types.Message, state: FSMContext):
    """Получение от пользователя его номера телефона."""
    contact = message.contact
    # Проверка на подлинность номера телефона пользователя.
    if message.from_user.id == contact.user_id:
        async with state.proxy() as data:
            data['phone_number'] = contact.phone_number
        await message.answer(
            'Ваш номер телефона принят.\n'
            'Введите пароль для регистрации.',
            reply_markup=ReplyKeyboardRemove()
        )
        await Register.password.set()
    else:
        await message.answer('Это не ваш номер телефона!')


@clearance_level(const.UNREGISTERED_USER)
@dp.message_handler(
    state=Register.password, content_types=types.ContentType.TEXT
)
async def get_password(message: types.Message, state: FSMContext):
    """Получение пароля для регистрации."""
    session = db.create_session()
    password_user = message.text
    bot_me = await bot.get_me()
    password_system = session.query(models.Config.tgc_password).filter(
        models.Config.tgc_bot_login == bot_me.username
    ).first()[0]
    if password_system == password_user:
        await message.answer('Ваши данные вносятся в базу данных.')
        await db.add_user(message, state)
        await message.answer('Регистрация прошла успешно.')
    else:
        await message.answer('Неправильный пароль')
    await state.finish()
