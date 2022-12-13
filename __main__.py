import asyncio
import logging
import os

from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


from air_quality_bishkek.handlers import register_handlers
from air_quality_bishkek.gidromet_scrapper import GidrometData, get_mapdata


async def on_startup(dispatcher:Dispatcher):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_mapdata,IntervalTrigger(start_date=datetime.now(),hours=1),next_run_time=datetime.now(),args=(gidromet_state,))
    scheduler.start()
    await dp.bot.set_my_commands([
        types.BotCommand('/start','Начало работы с ботом'),
        types.BotCommand('/about_aqi','Справка об AQI')
    ])
    
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher:Dispatcher):
    await bot.session.close()
    await bot.delete_webhook()


logger = logging.Logger(__name__,logging.INFO)
f_handler = logging.StreamHandler()
f_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


TOKEN = os.getenv('BOT_TOKEN')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


gidromet_state:list[GidrometData] = []
bot = Bot(TOKEN)
bot['gidromet_state'] = gidromet_state
bot['logger'] = logger
dp = Dispatcher(bot)

register_handlers(dp)


start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


