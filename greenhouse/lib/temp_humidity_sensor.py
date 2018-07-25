#import Adafruit_DHT as ada
from datetime import datetime
import pytz
from tools.connection import Connection

class TempHumiditySensor():
    """Reads the humidity and temperature in celsius and returns it as a dictionary"""
    def __init__(self):
        self.measure()

    @staticmethod
    def measure():
        """Read the humidity and celsius temperature reading from the hardware.
           Convert the celsius reading to farenheight.
           Return it as a tuple"""
        convert_to_farenheight = lambda x: x * 9/5 + 32
        now = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone("US/Pacific")).strftime("%Y-%m-%d %H:%M:%S")

        try:
            humidity, celsius = ada.read_retry(ada.AM2302, 4)
            return {
                'humidity_sensor': {
                    'task': 'humidity_sensor',
                    'status': 'success',
                    'value_numeric': humidity,
                    'value_enum': None,
                    'timestamp': now},
                'temperature_sensor': {
                    'task': 'temperature_sensor',
                    'status': 'success',
                    'value_numeric': convert_to_farenheight(celsius),
                    'value_enum': None,
                    'timestamp': now},
            }
        except BaseException as err:
            return {
                'humidity_sensor': {
                    'task': 'humidity_sensor',
                    'status': 'failure',
                    'value_numeric': None,
                    'value_enum': None,
                    'timestamp': now},
                'temperature_sensor': {
                    'task': 'temperature_sensor',
                    'status': 'failure',
                    'value_numeric': None,
                    'value_enum': None,
                    'timestamp': now},
            }

if __name__ == '__main__':
    TempHumiditySensor()
