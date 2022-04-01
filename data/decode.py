from pyzbar.pyzbar import decode
from PIL import Image
import io


def decode_image(bytes_image: io.BytesIO) -> str:
    """Декодирует переданное изображения в виде байтов
    и возвращает его значения."""
    with Image.open(bytes_image) as image:
        data_barcode = decode(image)[0].data.decode('utf-8')
    return data_barcode
