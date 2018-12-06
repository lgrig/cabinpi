import time
from lib.relay_switch import RelaySwitch

def turn_on_tub(self):
    RelaySwitch(gpio_pin=18).switch_on()

def turn_off_tub(self):
    RelaySwitch(gpio_pin=18).switch_off()
