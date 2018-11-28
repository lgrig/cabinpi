""" LOGIC PRIORITY
1. Manual switch > all else
2. Temperature Cycle > Time Cycle
3. Time Cycle
"""
from datetime import datetime, timedelta
import time
from lib.relay_switch import RelaySwitch
from lib.water_temperature import WaterTemperature
from multiprocess import Process

#Create a worker process to take inputs for the hot tub

class HotTub():
    def __init__(self, relay_pin=None, water_temp_pin=None):
        self.relay_pin = relay_pin
        self.water_temp_pin = water_temp_pin

    @staticmethod
    def start_process()
    proc = multiprocessing.Process(target=worker, args=name='tub daemon')
    proc.daemon = True
    proc.start()

    @staticmethod
    def worker(input_dict=None):
        relay_switch['task']()

if __name__ == '__main__':
    proc = multiprocessing.Process(target=worker, name='tub daemon')
    proc.daemon = True
    proc.start()
