from aiogram import Bot, Dispatcher, executor, types

bot = Bot("5681963298:AAEEmqz66B0fx3kU5ZroYK0Tyr-hVHln9ZE")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start','help'])
async def send_hello(message:types.Message):
    await message.reply("Это бот который отражает погоду и другую полезную информацию об окружающей среде в Бишкеке на данный момент")

def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton("Share Position", request_location=True)
    keyboard.add(button)
    return keyboard

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    reply = "latitude:  {}\nlongitude: {}".format(lat, lon)
    await message.answer(reply)

@dp.message_handler(commands=['locate_me'])
async def cmd_locate_me(message: types.Message):
    reply = "Click on the the button below to share your location"
    await message.answer(reply, reply_markup=get_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp)
