import datetime
import logging
from aiogram import types
from aiogram.utils import exceptions
import PIL

from loader import dp, bot
from data.decode import decode_image
from data import config
from utils.db_api.db_session import DataBase
from utils.misc import clearance_level


db = DataBase()


@clearance_level()
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def decode_photo(message: types.Message):
    """Обработчик декодирования фото со штрих кодом."""
    file_id = message.photo[-1].file_id
    config_db = await db.get_config(config.BOT_LOGIN)
    try:
        bytes_file = await bot.download_file_by_id(
            file_id
        )
        if config_db.tgc_path_photo is not None and config_db.tgc_path_photo:
            try:
                filename = datetime.datetime.now()
                path_download_file = f'{config_db.tgc_path_photo}/' \
                                     f'{filename}.png'
                await message.photo[-1].download(
                    destination_file=path_download_file
                )
                logging.info('The file was saved successfully.')
            except Exception:
                logging.warning(
                    f'Failed to save file. '
                    f'Check if the path is correct '
                    f'("{config_db.tgc_path_photo}").'
                )

        data_barcode = decode_image(bytes_file)
        logging.info('Image decoded successfully.')
        logging.debug(f'Image decoded: {data_barcode}')
        barcode_data = await db.get_data_barcode(data_barcode)
        await message.answer(barcode_data)
        await db.create_log_entry(message, path_photo=path_download_file)
    except TypeError:
        logging.info('Incorrect barcode.')
        await db.create_log_entry(message, 2)
        await message.answer('Такой штрих-код не был найден в базе данных')
    except PIL.UnidentifiedImageError:
        logging.info('Images are not the correct format.')
        await db.create_log_entry(message, 4)
        await message.answer(
            'Неправильный формат изображения.'
        )
    except IndexError:
        logging.info('Barcode on image not found.')
        await db.create_log_entry(message, 2)
        await message.answer(
            'Штрих-код не найден.'
        )
    except exceptions.FileIsTooBig:
        logging.info('File is too big.')
        await db.create_log_entry(message, 3)
        await message.answer(
            'Файл слишком большой.'
        )
