import logging
from datetime import datetime

from aiogram.types import PhotoSize

from data import exceptions


async def create_file(
        photo: PhotoSize, path_file: str
) -> str:
    """Создает файл-png с именем дата-время."""
    filename = datetime.now()
    path_download_file = f'{path_file}/{filename}.png'
    try:
        await photo.download(
            destination_file=path_download_file
        )
    except Exception:
        raise exceptions.FiledSaveFile()
    logging.info('The file was saved successfully.')
    return path_download_file
