"""Relay Switch class"""
from datetime import datetime
from gpiozero import LED
import pytz

tz = pytz.timezone('UTC').astimezone(pytz.timezone("US/Pacific"))
now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

#we will need to be constantly feeding the gpio pin current for it to be active

class RelaySwitch:
    """Relay switch class"""
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self.relay = LED(self.gpio_pin)

    def switch(self, value=None):
        """Turn on the relay switch, it will continue to run"""
        try:
            return {
                'relay_switch_on': {
                    'task': 'relay_switch_on',
                    'status': 'success',
                    'value_numeric': value,
                    'value_enum': 'gpio pin {}'.format(self.gpio_pin),
                    'timestamp': now}
            }

        except BaseException as err:
            return {
                'relay_switch_on': {
                    'task': 'relay_switch',
                    'status': 'failure',
                    'value_numeric': value,
                    'value_enum': 'gpio pin {}'.format(self.gpio_pin),
                    'timestamp': now}
            }
