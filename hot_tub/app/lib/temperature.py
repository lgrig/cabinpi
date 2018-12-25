"""
https://github.com/timofurrer/w1thermsensor
The default data pin is GPIO4 (RaspPi connector pin 7), but that can be changed from 4 to x with dtoverlay=w1-gpio,gpiopin=x.
"""
import re
import rq
from redis import Redis
from app.models import WaterTemp, BoxTemp
from app.lib import rpi_job
from app import db
from lib import rpi_job
from w1thermsensor import W1ThermSensor
from time import sleep
from datetime import datetime
import Adafruit_DHT
logger = rpi_job.logger

water = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, '00000a99d508')
box = Adafruit_DHT.AM2302

class Temperature(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()

    def record_water_temp(self):
        """Water temperature sensor works off of the 1-Wire parasitic setup.
        start here - http://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
        dtoverly settings differ from those shown in this tutorial.
        """
        temp_f = water.get_temperature(W1ThermSensor.DEGREES_F)
        db.session.add(WaterTemp(temperature_f=temp_f, create_datetime=datetime.now()))
        db.session.commit()

    def record_box_temp(self, pin=17):
        """Box temp is recorded to ensure that the solid state relay isn't overheating.
           If it overheats and burns down the house, that would suck.
           Because the 1-wire runs correctly on GPIO 4, we moved this one to GPIO 17

           This module seems to hang if called too frequently, so there's a delay added at the end
        """
        humidity, temp_c = Adafruit_DHT.read_entry(box, pin)
        temp_f = temp_c * 9/5.0 + 32
        db.session.add(Boxtemp(temperature_f=temp_f, create_datetime=datetime.now()))

#RQ Worker Server setup
def water_temp_server():
    """looks for a redis worker called 'hot_tub_temp' and assigns the background job forever"""
    queue = rq.Queue('hot_tub_temp', connection=Redis.from_url('redis://'))
    job = queue.enqueue(check_water_temp(),-1)

def box_temp_server():
    """looks for a redis worker called 'hot_tub_temp' and assigns the background job forever"""
    queue = rq.Queue('hot_tub_temp', connection=Redis.from_url('redis://'))
    job = queue.enqueue(check_box_temp(),-1)

def check_water_temp():
    """Background job that is constantly measuring and recording water temperature
       Time delay in the file i/o is long enough to not need sleep instructions"""
    while True:
        Temperature().record_water_temp()

def check_box_temp():
    """Background job that is constantly measuring and recording water temperature
       Time delay in the file i/o is long enough to not need sleep instructions"""
    while True:
        Temperature().record_box_temp()

def check_temps():
    """Background job that is constantly measuring and recording temperatures"""
    while True:
        try:
            Temperature().record_water_temp()
        except BaseException as err:
            logger.error(err)

        try:
            Temperature().record_box_temp()
        except BaseException as err:
            logger.error(err)

        sleep(2)

if __name__ == '__main__':
    check_water_temp()
