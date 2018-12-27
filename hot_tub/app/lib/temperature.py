"""
https://github.com/timofurrer/w1thermsensor
The default data pin is GPIO4 (RaspPi connector pin 7), but that can be changed from 4 to x with dtoverlay=w1-gpio,gpiopin=x.
"""
import re
import rq
from redis import Redis
from app.models import WaterTemp, BoxTemp
from app.lib.admin import rpi_job
from app import db
from w1thermsensor import W1ThermSensor
from time import sleep
from datetime import datetime
from pytz import timezone
import Adafruit_DHT
logger = rpi_job.logger

water = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, '00000a99d508')
box = Adafruit_DHT.AM2302

class Temperature(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()

    def record_water_temp(self, rec_time=None):
        """Water temperature sensor works off of the 1-Wire parasitic setup.
        start here - http://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
        dtoverly settings differ from those shown in this tutorial.
        """
        temp_f = round(water.get_temperature(W1ThermSensor.DEGREES_F), 2)
        db.session.add(WaterTemp(temperature_f=temp_f, create_datetime=rec_time))
        db.session.commit()
        return temp_f

    def record_box_temp(self, pin=17, rec_time=None):
        """Box temp is recorded to ensure that the solid state relay isn't overheating.
           If it overheats and burns down the house, that would suck.
           Because the 1-wire runs correctly on GPIO 4, we moved this one to GPIO 17

           This module seems to hang if called too frequently, so there's a delay added at the end
        """
        humidity, temp_c = Adafruit_DHT.read_retry(box, pin)
        if temp_c and temp_c > 0:
            temp_f = round(temp_c * 9/5.0 + 32, 2) if temp_c else None
            db.session.add(BoxTemp(temperature_f=temp_f, create_datetime=rec_time))
            return temp_f

    def clear_temperatures(self):
        db.session.execute("DELETE FROM water_temp;")
        db.session.execute("DELETE FROM box_temp;")
        db.session.commit()

def check_temps():
    """Background job that is constantly measuring and recording temperatures.
       Lined up the times to make the graphs prettier"""
    while True:
        rec_time = datetime.now(timezone('America/Los_Angeles'))
        try:
            wtmp = Temperature().record_water_temp(rec_time=rec_time)
        except BaseException as err:
            logger.error(err)

        try:
            btmp=Temperature().record_box_temp(rec_time=rec_time)
        except BaseException as err:
            logger.error(err)
        sleep(2)

if __name__ == '__main__':
    check_temps()
