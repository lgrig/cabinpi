"""Relay Switch class"""
from datetime import datetime
from time import sleep
import gpiozero
from gpiozero.pins import Factory
import pytz

time = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone("US/Pacific"))
now = time.strftime("%Y-%m-%d %H:%M:%S")

#we will need to be constantly feeding the gpio pin current for it to be active
class RelaySwitch:
    """Relay switch class"""
    def __init__(self, gpio_pin=None):
        self.gpio_pin = gpio_pin
        self.relay = gpiozero.LED(self.gpio_pin)

    def switch_on(self):
        """Turn on the relay switch, it will continue to run"""
        return {
                'task': self.relay.on,
                'value_numeric': 1,
                'value_enum': 'gpio pin {}'.format(self.gpio_pin),
                'timestamp': now
        }

    def switch_off(self):
        """Turn on the relay switch, it will continue to run"""
        self.relay.off()
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
