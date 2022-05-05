import logging

import PIL
from aiogram.types import Update
from sqlalchemy.exc import ProgrammingError, DataError
from aiogram.utils.exceptions import (TelegramAPIError,
                                      MessageNotModified,
                                      CantParseEntities, CantDemoteChatCreator,
                                      MessageCantBeDeleted,
                                      MessageToDeleteNotFound,
                                      MessageTextIsEmpty, Unauthorized,
                                      InvalidQueryID, RetryAfter, FileIsTooBig)


from loader import dp
from data import exceptions
from utils.db_api.db_session import DataBase

db = DataBase()


@dp.errors_handler()
async def errors_handler(update, exception):
    """Обработчик ошибок."""
    message = Update.get_current().message

    if isinstance(exception, exceptions.NotFoundBarcode):
        logging.info('Barcode on image not found.')
        await db.create_log_entry(message, 2)
        await message.answer(
            'Штрих-код не найден на изображении.'
        )
        return True

    if isinstance(exception, DataError):
        logging.error('Invalid barcode data type.')
        await message.answer('Неправильный тип данных штрих-кода.')
        return True

    if isinstance(exception, ProgrammingError):
        logging.error(f'Incorrect sql query: {exception}')
        await message.answer('Не удалось запросить данные.')
        return True

    if isinstance(exception, exceptions.InvalidTypeInsert):
        logging.error(f'Incorrect sql query: {exception}')
        await message.answer('Не удалось запросить данные.')
        return True

    if isinstance(exception, exceptions.LowLevelPermission):
        await message.answer('Вы не обладаете нужными правами.')
        await db.create_log_entry(message, 5)
        return True

    if isinstance(exception, exceptions.Spam):
        await message.answer('Вы слишком часто пишите.')
        return True

    if isinstance(exception, PIL.UnidentifiedImageError):
        logging.info('Images are not the correct format.')
        await db.create_log_entry(message, 4)
        await message.answer(
            'Неправильный формат изображения.'
        )
        return True

    if isinstance(exception, exceptions.UnknownBarcode):
        logging.info('Incorrect barcode.')
        await db.create_log_entry(message, 2)
        await message.answer('Такой штрих-код не был найден в базе данных')
        return True

    if isinstance(exception, FileIsTooBig):
        logging.info('File is too big.')
        await db.create_log_entry(message, 3)
        await message.answer(
            'Файл слишком большой.'
        )
        return True

    if isinstance(exception, CantDemoteChatCreator):
        logging.exception("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logging.exception('Message is not modified')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        logging.exception('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.exception('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.exception('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.exception(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
      
    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    logging.exception(f'Update: {update} \n{exception}')
