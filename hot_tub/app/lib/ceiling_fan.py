"""
    Ceiling fan runs off of what looks like a 433Mhz controller
    Goal is to control the ceiling fan by google assistant command
    Google assistant library is here: https://developers.google.com/assistant/sdk/guides/library/python/
"""

from app.lib.rpi_job import RPIJob
from app.models import GPIOTask
from app import db
from datetime import datetime

class CeilingFan(RPIJob):
    def __init__(self):
        super().__init__()

    def write_db(self):
        """There are 5 different commands:
            1. Light on
            2. Light off
            3. Fan Off
            4. Fan Speed 1
            5. Fan Speed 2
            6. Fan Speed 3
        """
        payload = lambda enum, num: {
            'name': 'ceiling_fan', 'status_enum': {enum}, 'status_numeric': {num},
            'description': 'ceiling_fan_action_sent', 'create_datetime': datetime.now()}

        instructions_map = {
            'light_on': {'enum': 'light_off', 'num': 0}, 'light_on': {'enum': 'light_on', 'num': 1},
            'fan_off': {'enum': 'fan_off', 'num': 2}, 'fan_level_1': {'enum': 'fan_level_1', 'num': 3},
            'fan_level_2': {'enum': 'fan_level_2', 'num': 4}, 'fan_level_3': {'enum': 'fan_level_3', 'num': 5},
        }
