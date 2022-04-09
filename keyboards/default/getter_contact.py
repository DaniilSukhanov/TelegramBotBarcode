from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


keyboard_getter_contact = ReplyKeyboardMarkup(
    [[KeyboardButton('Прислать номер телефона', request_contact=True)]]
)
