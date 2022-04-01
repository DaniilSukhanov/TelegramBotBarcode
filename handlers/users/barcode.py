from aiogram import types
from aiogram.utils import exceptions

from loader import dp, bot
from data.decode import decode_image
import PIL


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def decode_photo(message: types.Message):
    """"""
    file_id = message.photo[-1].file_id
    try:
        bytes_file = await bot.download_file_by_id(file_id)
        data_barcode = decode_image(bytes_file)
        await message.answer(data_barcode)
    except PIL.UnidentifiedImageError:
        await message.answer(
            'Неправильный тип файла.'
        )
    except IndexError:
        await message.answer(
            'Штрих-код не найден.'
        )
    except exceptions.FileIsTooBig:
        await message.answer(
            'Файл слишком большой.'
        )
