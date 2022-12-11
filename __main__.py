import asyncio
import logging

from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from air_quality_bishkek.handlers import register_handlers
from air_quality_bishkek.gidromet_scrapper import GidrometData, get_mapdata
from config import BOT_TOKEN


async def main():
    logger = logging.Logger(__name__,logging.ERROR)
    f_handler = logging.FileHandler('weather_bot.log')
    f_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    try:
        gidromet_state:list[GidrometData] = []
        bot = Bot(BOT_TOKEN)
        bot['gidromet_state'] = gidromet_state
        bot['logger'] = logger
        dp = Dispatcher(bot)

        scheduler = AsyncIOScheduler()
        scheduler.add_job(get_mapdata,IntervalTrigger(start_date=datetime.now(),hours=1),next_run_time=datetime.now(),args=(gidromet_state,))
        scheduler.start()

        register_handlers(dp)

        await dp.bot.set_my_commands([
                types.BotCommand('/start','Начало работы с ботом'),
                types.BotCommand('/about_aqi','Справка об AQI')
            ])

        await dp.start_polling()
    finally:
        bot.session.close()


try:
    asyncio.run(main())
except (KeyboardInterrupt,SystemExit):
    print('Bot stopped')
