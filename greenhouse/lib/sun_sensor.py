from datetime import datetime
import pytz
import tsl2591
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
            tsl = tsl2591.Tsl2591()  # initialize
            full, ir = tsl.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
            lux = tsl.calculate_lux(full, ir)  # convert raw values to lux
            return {'task': 'sun_reading',
                    'status': 'success',
                    'value_numeric': lux,
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
