from pyzbar.pyzbar import decode
from PIL import Image
import io
from . import exceptions


def decode_image(bytes_image: io.BytesIO) -> str:
    """Декодирует переданное изображения в виде байтов
    и возвращает его значения."""
    with Image.open(bytes_image) as image:
        list_decode = decode(image)
        if not list_decode:
            raise exceptions.NotFoundBarcode()
        data_barcode = list_decode[0].data.decode('utf-8')
    return data_barcode
