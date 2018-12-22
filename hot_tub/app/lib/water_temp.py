"""
   https://github.com/timofurrer/w1thermsensor

The following hardware is needed:

w1 therm compatible sensor (some of them can be bought here: Adafruit: DS18B20)
wires to connect the sensor to your board (you might need a breadboard, too)
a board like the Raspberry Pi or the Beagle Bone)
On the Raspberry Pi, you will need to add dtoverlay=w1-gpio" (for regular connection) or dtoverlay=w1-gpio,pullup="y" (for parasitic connection) to your /boot/config.txt.

The default data pin is GPIO4 (RaspPi connector pin 7), but that can be changed from 4 to x with dtoverlay=w1-gpio,gpiopin=x.
"""
import re
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
        print(temp_f)
        db.session.add(WaterTemp(temperature_f=temp_f, create_datetime=datetime.now()))
        db.session.commit()

def temperature_server(self):
    """looks for a redis worker called 'hot_tub_temp' and assigns the background job forever"""
    queue = rq.Queue('hot_tub_temp', connection=Redis.from_url('redis://'))
    job = queue.enqueue('app.lib.water_temp.check_temp', -1)

def check_temp(self):
    """Background job that is constantly measuring and recording water temperature
       Time delay in the file i/o is long enough to not need sleep instructions"""
    while True:
        Temperature().record_temperature()

if __name__ == '__main__':
    Temperature().record_temperature()
