from datetime import datetime
import pytz
from tools.connection import Connection

class SunSensor():
    """Reads the soil moisture level and returns it as a dictionary"""
    def __init__(self):
        pass

    @staticmethod
    def measure():
        """Read the soil moisture level and return it as a dictionary"""
        now = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone("US/Pacific")).strftime("%Y-%m-%d %H:%M:%S")
        try:
            sun_reading = None
            return {'task': 'sun_reading',
                    'status': 'success',
                    'value_numeric': sun_reading,
                    'value_enum': None,
                    'timestamp': now}
        except BaseException as err:
            return {'task': 'sun_reading',
                    'status': 'failure',
                    'value_numeric': None,
                    'value_enum': None,
                    'timestamp': now}

if __name__ == '__main__':
    SunSensor().measure()
