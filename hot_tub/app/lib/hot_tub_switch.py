"""Relay Switch Class: create server to read changes to the database
   If a change is detected, adjust the pin accordingly.
   Start up should take the last pin position and run pins accordingly.
"""
from app.models import GPIOTask
from app import db
from lib.admin import rpi_job
from datetime import datetime

class HotTubSwitch(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()
        self.template = {'name': 'hot_tub', 'status_enum': None, 'status_numeric': None, 'description': None, 'create_datetime': datetime.now()}

    def turn_on_hot_tub(self):
        rec = self.template
        rec['status_enum'], rec['status_numeric'], rec['description'] = 'on', 1, 'turn on tub'
        db.session.add(GPIOTask(**rec))
        db.session.commit()

    def turn_off_hot_tub(self):
        """Turn on the relay switch, it will continue to run"""
        rec = self.template
        rec['status_enum'], rec['status_numeric'], rec['description'] = 'off', 0, 'turn off tub'
        db.session.add(GPIOTask(**rec))
        db.session.commit()
