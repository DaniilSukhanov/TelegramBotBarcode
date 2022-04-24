import datetime
import logging
from aiogram import types
import PIL

from loader import dp, bot
from data.decode import decode_image
from data import config, exceptions
from utils.db_api.db_session import DataBase
from utils.misc import clearance_level
from utils.misc.create_file import create_file

db = DataBase()


@clearance_level()
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def decode_photo(message: types.Message):
    """Обработчик декодирования фото со штрих кодом."""
    file_id = message.photo[-1].file_id
    config_db = await db.get_config(config.BOT_LOGIN)
    bytes_file = await bot.download_file_by_id(
        file_id
    )
    path_download_file = None
    if config_db.tgc_path_photo is not None and config_db.tgc_path_photo:
        try:
            path_download_file = await create_file(
                message.photo[-1], config_db.tgc_path_photo
            )
        except exceptions.FiledSaveFile:
            logging.info('Failed to save file.')

    data_barcode = decode_image(bytes_file)
    logging.info('Image decoded successfully.')
    logging.debug(f'Image decoded: {data_barcode}')
    response = await db.get_data_barcode(data_barcode)
    await message.answer(response)
    await db.create_log_entry(message, path_photo=path_download_file)
