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

    def turn_on_hot_tub(self):
        db.session.add(GPIOTask('hot_tub', 'on', 1, 'turn on tub', datetime.now()))
        db.session.commit()

    def turn_off_hot_tub(self):
        """Turn on the relay switch, it will continue to run"""
        db.session.add(GPIOTask('hot_tub', 'off', 0, 'turn off tub', datetime.now()))
        db.session.commit()
