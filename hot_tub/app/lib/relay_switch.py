"""Relay Switch Class: create server to read changes to the database
   If a change is detected, adjust the pin accordingly.
   Start up should take the last pin position and run pins accordingly.
"""
from app.models import GPIOTask
from app import db
from lib import rpi_job
from datetime import datetime

class RelaySwitch(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()
        self.template = {'name': 'hot_tub', 'status_enum': None, 'status_numeric': None, 'description': None, 'create_datetime': datetime.now()}

    def turn_on_hot_tub(self):
        record = self.template.update({'status_enum': 'on', 'status_numeric': 1, 'description': 'turn on tub'})
        db.session.add(GPIOTask(**record))
        db.session.commit()

    def turn_off_hot_tub(self):
        """Turn on the relay switch, it will continue to run"""
        record = self.template.update({'status_enum': 'off', 'status_numeric': 0, 'description': 'turn off tub'})
        db.session.add(GPIOTask(**record))
        db.session.commit()
