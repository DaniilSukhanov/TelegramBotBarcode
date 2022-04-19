import logging
from aiogram import types
from aiogram.utils import exceptions
import PIL

from loader import dp, bot
from data.decode import decode_image
from utils.db_api.db_session import DataBase
from utils.misc import clearance_level


db = DataBase()


@clearance_level()
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def decode_photo(message: types.Message):
    """Обработчик декодирования фото со штрих кодом."""
    file_id = message.photo[-1].file_id
    try:
        bytes_file = await bot.download_file_by_id(file_id)
        data_barcode = decode_image(bytes_file)
        logging.info('Image decoded successfully.')
        logging.debug(f'Image decoded: {data_barcode}')
        barcode_data = await db.get_data_barcode(data_barcode)
        await message.answer(barcode_data)
    except TypeError:
        logging.info('Incorrect barcode.')
        await message.answer('Такой штрих-код не был найден в базе данных')
    except PIL.UnidentifiedImageError:
        logging.info('Images are not the correct format.')
        await message.answer(
            'Неправильный формат изображения.'
        )
    except IndexError:
        logging.info('Barcode on image not found.')
        await message.answer(
            'Штрих-код не найден.'
        )
    except exceptions.FileIsTooBig:
        logging.info('File is too big.')
        await message.answer(
            'Файл слишком большой.'
        )
