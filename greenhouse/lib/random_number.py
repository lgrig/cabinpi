""" Tester Class for post request """
import random
import json
import pytz
from datetime import datetime

class RandomNumber:
    def __init__(self):
        pass

    @staticmethod
    def measure():
        now = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone("US/Pacific")).strftime("%Y-%m-%d %H:%M:%S")
        num = random.randint(1, 101)
        try:
            return json.dumps({
                'random_number': {
                    'task': 'gen_random_number',
                    'status': 'success',
                    'value_numeric': num,
                    'value_enum': None,
                    'timestamp': now}
                })

        except BaseException as err:
            return json.dumps({
                'random_number': {
                    'task': 'gen_random_number',
                    'status': 'failure',
                    'value_numeric': None,
                    'value_enum': None,
                    'timestamp': now}
                })
