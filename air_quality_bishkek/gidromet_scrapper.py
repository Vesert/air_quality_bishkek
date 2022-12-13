import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import dataclasses
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logger=logging.Logger(name = __name__,level=logging.INFO)
f_handler = logging.StreamHandler('gidromet_scrapper.log')
f_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

@dataclasses.dataclass
class GidrometData:
    sensor_name: str = None
    color: str = None
    latitude:float = None
    longitude:float=None
    measured_at:datetime=None
    pm1:float=None
    pm10:float=None
    pm25:float=None
    no:float=None
    no2:float=None
    ch2o:float=None
    so2:float=None
    aqius:float=None
    temperature:float=None
    humidity:float=None
    pressure:float=None

    def __post_init__(self):
        self.latitude = float(self.latitude) if self.latitude is not None else None
        self.longitude = float(self.longitude) if self.longitude is not None else None
        self.measured_at = datetime.fromtimestamp(self.measured_at) if self.measured_at is not None else None
        self.pm1 = float(self.pm1) if self.pm1 is not None else None
        self.pm10 = float(self.pm10) if self.pm10 is not None else None
        self.pm25 = float(self.pm25) if self.pm25 is not None else None
        self.no = float(self.no) if self.no is not None else None
        self.no2 = float(self.no2) if self.no2 is not None else None
        self.ch2o = float(self.ch2o) if self.ch2o is not None else None
        self.so2 = float(self.so2) if self.so2 is not None else None
        self.aqius = float(self.aqius) if self.aqius is not None else None
        self.temperature = float(self.temperature) if self.temperature is not None else None
        self.humidity = float(self.humidity) if self.humidity is not None else None
        self.pressure = float(self.pressure) if self.pressure is not None else None
    
    def __call__(self,*args,**kwargs):

        self.__init__(*args,**kwargs)

    def _get_aqi_color(self):
        if self.aqius <=50:
            return '\U0001F7E2'
        elif self.aqius <=100:
            return '\U0001F7E1'
        elif self.aqius <= 150:
            return '\U0001F7E0'
        elif self.aqius <= 200:
            return '\U0001F534'
        elif self.aqius <= 300:
            return '\U0001F7E4'
        else:
            return '\U0001F7E3'

    def __str__(self):
        return '\n'.join(('\U0001F321 Температура(°C): '+str(self.temperature),
        '\U0001F4A7 Влажность воздуха(%): ' + str(self.humidity),
        '\U0001F637 AQI: '+str(self.aqius) + ' '+ self._get_aqi_color(),
        ))


async def get_mapdata(gidromet_state:list[GidrometData]):
    
    gidromet_state.clear()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://air.meteo.kg/ru") as result:
                air_quality_page = await result.read()
                mapdata = BeautifulSoup(air_quality_page)\
                .find("div",id="mapdata")\
                .text

                for gidromet_elem in  json.loads(mapdata):
                    gidromet_state.append(GidrometData(**gidromet_elem))
        logger.info('gidromet scrapped',len(gidromet_state))
    except aiohttp.ClientError:
        loggier.exception('Get_mapdata in trouble')