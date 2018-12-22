"""
https://github.com/timofurrer/w1thermsensor
The default data pin is GPIO4 (RaspPi connector pin 7), but that can be changed from 4 to x with dtoverlay=w1-gpio,gpiopin=x.
"""
import re
import rq
from redis import Redis
from app.models import WaterTemp
from app.lib import rpi_job
from app import db
from lib import rpi_job
from w1thermsensor import W1ThermSensor
from datetime import datetime
logger = rpi_job.logger

sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, '00000a99d508')

class Temperature(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()

    def record_temperature(self):
        temp_f = sensor.get_temperature(W1ThermSensor.DEGREES_F)
        db.session.add(WaterTemp(temperature_f=temp_f, create_datetime=datetime.now()))
        db.session.commit()

#RQ Worker Server setup
def temperature_server():
    """looks for a redis worker called 'hot_tub_temp' and assigns the background job forever"""
    queue = rq.Queue('hot_tub_temp', connection=Redis.from_url('redis://'))
    job = queue.enqueue(check_temp(),-1)

def check_temp():
    """Background job that is constantly measuring and recording water temperature
       Time delay in the file i/o is long enough to not need sleep instructions"""
    while True:
        Temperature().record_temperature()

if __name__ == '__main__':
    check_temp()
