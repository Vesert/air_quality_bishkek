from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from .keyboards import get_keyboard
from haversine import haversine

async def send_hello(message:types.Message):
    try:
        full_name = message.from_user.full_name
        answer_text = (
        f'Здравствуйте <b>{full_name}</b>!\n\n'
        'Это бот который отражает температуру, влажность воздуха и индекс AQI в Бишкеке на данный момент на ближайшем к вашему местоположению датчике.\n\n'
        '<b>"Поделиться позицией"</b> для получения данных с ближайшего к вам датчика\n'
        '<b>"Подробнее об AQI"</b> для получения справки об цветовой индикации AQI\n'
        '<b>"Помощь"</b> для общей справки\n'
        '🇰🇬🇰🇬🇰🇬🇰🇬🇰🇬🇰🇬🇰🇬🇰🇬🇰🇬🇰🇬🇰🇬')
        await message.answer(text=answer_text,parse_mode='HTML',reply_markup = get_keyboard())
    except TelegramAPIError:
        message.bot.logger.exception('some troubles in hello')


async def send_aqi_desc(message:types.Message):
    try:
        answer_text = (
            'AQI - индекса качества воздуха.\n'
            'Для расчета AQI учитываются шесть основных загрязнителей воздуха: твердые частицы (PM 10 и PM 2,5), окись углерода (CO), озон (O3), двуокись азота (NO2) и двуокись серы (SO2).\n\n'
            'Цветовая шкала:\n'
            '\U0001F7E2 - не представляет опасности для здоровья\n'
            '\U0001F7E1 - чувствительные группы должны значительно сократить прогулки на свежем воздухе и избегать проветривания помещений наружным воздухом (относится к детям, пожилым людям, беременным, людям с сердечными и легочными заболеваниями)\n'
            '\U0001F7E0 - все подвергаются риску раздражения глаз, кожи и горла, а также респираторных заболеваний\n'
            '\U0001F534 - существует повышенная вероятность ухудшения состояния сердца и легких (с этого момента на улице следует носить маску)\n'
            '\U0001F7E4 - заметное влияние на население\n'
            '\U0001F7E3 - каждый подвергается высокому риску сильного раздражения и негативных последствий для здоровья, которые могут спровоцировать сердечно-сосудистые и респираторные заболевания.\n'
        )
        await message.answer (text=answer_text,parse_mode='HTML',reply_markup = get_keyboard())
    except TelegramAPIError:
        message.bot.logger.exception('some troubles in aqi_desc')



async def handle_location(message: types.Message):
    try:
        gidromet_state = message.bot.get('gidromet_state')
        user_loc = message.location.latitude, message.location.longitude
        max_distance = None
        new_distance = None
        min_dist_station_index = 0
        for pos,station_data in enumerate(gidromet_state):
            station_loc = station_data.latitude,station_data.longitude
            if pos==0:
                max_distance = haversine(user_loc,station_loc)
            else:
                new_distance = haversine(user_loc,station_loc)
            if new_distance is not None and new_distance < max_distance:
                max_distance = new_distance
                min_dist_station_index = pos
            
        reply = str(gidromet_state[min_dist_station_index])
        await message.answer(text=reply,reply_markup=get_keyboard())
    except TelegramAPIError:
        pass
        message.bot.logger.exception('Some troubles in handle_location')

def register_handlers(dp:Dispatcher):
    dp.register_message_handler(send_hello,commands=['start','help'])
    dp.register_message_handler(send_hello,Text(equals='Помощь'))
    dp.register_message_handler(send_aqi_desc,Text(equals='Подробнее об AQI'))
    dp.register_message_handler(send_aqi_desc,commands=['about_aqi'])
    dp.register_message_handler(handle_location,content_types=['location'])