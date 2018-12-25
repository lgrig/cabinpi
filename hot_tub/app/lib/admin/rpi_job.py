from datetime import datetime
from time import sleep
import os
import pytz
from app import db
from app.lib.admin.logger import Logger
logger = Logger().get_logger()

is_rpi = 'arm' in os.uname()[4][:3]
if is_rpi:
    try:
        import gpiozero
        from gpiozero.pins import Factory
        import RPi.GPIO as GPIO
    except BaseException as err:
        logger.info(err)

class RPIJob:
    def __init__(self):
        self.is_rpi = True if 'arm' in os.uname()[4][:3] else False
