"""Relay Switch Class: create server to read changes to the database
   If a change is detected, adjust the pin accordingly.
   Start up should take the last pin position and run pins accordingly.
"""
from datetime import datetime
from time import sleep
import gpiozero
import RPi.GPIO as GPIO
from gpiozero.pins import Factory
import os
import pytz
from app import db
from app.models import GPIOTask
is_rpi = 'arm' in os.uname()[4][:3]
if is_rpi:
    import gpiozero
    from gpiozero.pins import Factory

class RelaySwitch:
    def __init__(self, gpio_pin=None):
        self.gpio_pin = gpio_pin
        if is_rpi:
            self.relay = gpiozero.LED(self.gpio_pin)
        else:
            self.relay = None

    def turn_on(self):
        db.session.add(GPIOTask('hot_tub', 'on', 1, 'turn on tub', datetime.now()))
        db.session.commit()

<<<<<<< HEAD
    def switch_on(self):
        """Turn on the relay switch, it will continue to run"""
        try:
            while True:
                self.relay.on()
        except BaseException as err:
            print(err)
        # return {
        #         'task': self.relay.on,
        #         'value_numeric': 1,
        #         'value_enum': 'gpio pin {}'.format(self.gpio_pin),
        #         'timestamp': now
        # }

    def switch_off(self):
        """Turn on the relay switch, it will continue to run"""
        GPIO.cleanup()
        return {
                'task': self.relay.off,
                'status': 'success',
                'value_numeric': 0,
                'value_enum': 'gpio pin {}'.format(self.gpio_pin),
                'timestamp': now
        }
if __name__ == '__main__':
    switch = RelaySwitch(gpio_pin=18)
    switch.switch_on()
    sleep(2)
    switch.switch_off()
    sleep(2)
=======
    def turn_off(self):
        db.session.add(GPIOTask('hot_tub', 'off', 0, 'turn off tub', datetime.now()))
        db.session.commit()

    def run_server(self):
        #poll the database every 5 seconds
        #if the database has been updated, trigger the GPIO pin
        while True:
            latest = GPIOTask.query.first()
            if latest.status_numeric == 1:
                self.relay.on()
            if latest.status_numeric == 0:
                self.relay.off()
            sleep(5)
>>>>>>> efc701d84cfa8b7961c0bdd138fe90a7323d6007
