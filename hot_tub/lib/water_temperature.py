"""Water temperature reading class"""
from datetime import datetime
import pytz

class WaterTemperature:
    def __init__(self):
        pass

    @staticmethod
    def measure():
        """Read the water temperature and return it as a dictionary"""
        time = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone("US/Pacific"))
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        water_temp_f = None

        try:
            return {
                'water_temperature': {
                    'task': 'water_temperature',
                    'status': 'success',
                    'value_numeric': water_temp_f,
                    'value_enum': None,
                    'timestamp': now
                }
            }
        except BaseException as err:
            return {
                'water_temperature': {
                    'task': 'water_temperature',
                    'status': 'failure',
                    'value_numeric': None,
                    'value_enum': None,
                    'timestamp': now
                }
            }
