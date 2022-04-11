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
    await message.answer(
        'Началась регистрация.\n'
        'Поделитесь своим номером телефона с ботом.',
        reply_markup=keyboard_getter_contact
    )
    await Register.phone_number.set()


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
        phone_number = (await state.get_data()).get('phone_number')
        await state.finish()
        tlg_user = message.from_user
        logging.info(
            f'Started adding the user {tlg_user.username} to the database.'
        )
        bot_id = session.query(models.Config.tgc_id).filter(
            models.Config.tgc_bot_login == bot_me.username
        ).first()[0]
        new_user = models.Users()
        new_user.tgu_user_id = str(tlg_user.id)
        new_user.tgu_name = tlg_user.first_name
        new_user.tgu_surname = tlg_user.last_name
        new_user.tgu_phone = phone_number
        new_user.tgu_login = tlg_user.username
        new_user.tgu_chat_id = message.chat.id
        new_user.tgu_bot_id = bot_id
        session.add(new_user)
        session.commit()
        logging.info(
            f'The user {tlg_user.username} has been added to the database.'
        )
        await message.answer('Регистрация прошла успешно.')
    else:
        await message.answer('Неправильный пароль')
