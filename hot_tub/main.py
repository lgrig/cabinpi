""" LOGIC PRIORITY
1. Manual switch > all else
2. Temperature Cycle > Time Cycle
3. Time Cycle
"""
from datetime import datetime, timedelta
import time
from lib.relay_switch import RelaySwitch
from lib.water_temperature import WaterTemperature

class HotTub():
    def __init__(self, relay_pin=None, water_temp_pin=None):
        self.relay_pin = relay_pin
        self.water_temp_pin = water_temp_pin

    def manual_switch_on_off(self, input_val=None):
        """input val is a string, 'on' or 'off'"""
        if input_val =='on':
            RelaySwitch(gpio_pin=self.relay_pin).switch(1)
        if input_val =='off':
            RelaySwitch(gpio_pin=self.relay_pin).switch(0)

    def safety_temperature_switch(self, safety_temp_f=40):
        while WaterTemperature().measure() < safety_temp_f:
            RelaySwitch(gpio_pin=self.relay_pin).switch(1)
            time.sleep(5)

    @staticmethod
    def ceil_dt(dt, delta):
        """Round time into x minute increments"""
        return dt + (datetime.min - dt) % delta

    def calendar_switch(self, run_duration=15):
        """if the current time is in the same 15 min as the ones listed below
           run the relay
        """
        #list of tuples, (run_time, duration_in_minutes)
        run_times = [
                {'time': '00:00:00'},
                {'time': '00:04:00'},
                {'time': '00:08:00'},
                {'time': '00:12:00'},
                {'time': '00:16:00'},
                {'time': '00:20:00'},
        ]
        check_times = [self.ceil_dt(t['time'], timedelta(minutes=run_duration)) for t in run_times]
        while self.ceil_dt(datetime.now(), timedelta(minutes=run_duration)) in check_times:
            RelaySwitch(gpio_pin=self.relay_pin).switch(1)
            time.sleep(5)
