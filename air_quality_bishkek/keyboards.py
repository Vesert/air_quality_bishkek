from aiogram import types

def get_keyboard():
    builder = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    builder.row(types.KeyboardButton("Поделиться позицией", request_location=True),
                types.KeyboardButton("Помощь"))
    builder.row(types.KeyboardButton("Подробнее об AQI"))
    return builder