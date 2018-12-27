"""Server to run on a redis worker and poll internal db for changes.
   If changes are found, execute scripts.
"""
from datetime import time
from datetime import datetime
import time as t
from pytz import timezone
import gpiozero

from app.models import WaterTemp, BoxTemp, GPIOTask
from app.lib.admin import rpi_job
from app.lib.admin.google_jobs import GoogleJobs
from app.lib.schedule import Schedule
from app.lib.hot_tub_switch import HotTubSwitch
from app.lib.temperature import Temperature
from app.lib.track_temperature import TrackTemperature
logger = rpi_job.logger
goog = GoogleJobs()

class RelayController(rpi_job.RPIJob):
    """Overall relay controller, runs a mock server on an infinite loop redis server.
       Class constantly polls local db and google docs for inputs to changes
    """
    def __init__(self, gpio_pin=18):
        super().__init__()
        self.relay = gpiozero.LED(gpio_pin) if self.is_rpi and gpio_pin else None

    def switch_tub(self, latest_record=None):
        """Execute gpio pin change to relay to start/stop 3v current"""
        cur_num = latest_record.status_numeric if latest_record else 0
        return self.relay.on() if bool(cur_num) else self.relay.off()

    def redis_server(self):
        """Server to watch for relevant databse changes"""
        box_temp, water_temp, latest_record = 0, 0, None
        #shut the whole thing down if the box breaks 100 degrees
        while box_temp < 100.00:
            #poll these less frequently, they require a google sheets server check
            try:
                Schedule().refresh_times()
                TrackTemperature().get_records()
                op_mode, safety_temp, laps = goog.get_operation_type(), goog.get_safety_temp(), 0
                water_temp = WaterTemp.query.order_by(WaterTemp.id.desc()).first().temperature_f
                box_temp = BoxTemp.query.order_by(BoxTemp.id.desc()).first().temperature_f
                latest_record = GPIOTask.query.order_by(GPIOTask.id.desc()).first()
                vals = [
                    ('B1', datetime.now(timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S')),
                    ('B2', str(water_temp)), ('B3', str(box_temp)), ('B4', latest_record.status_enum if latest_record else None)
                ]
                for val in vals:
                    goog.write_summary_value(*val)
                safety_flag = True if safety_temp > water_temp and safety_temp < 50 else False
                turn_on_conds = [
                        op_mode == 'Turn On',
                        safety_flag and safety_temp > water_temp,
                        not safety_flag and safety_temp > water_temp - 3,
                        bool(bool(Schedule().check_time()) and op_mode == 'Time Control')]
                logger.debug('temp below safety: {}, op_mode_on: {}, in_run_time_window: {}'.format(*turn_on_conds))

                turn_off_conds = [
                        op_mode == 'Turn Off',
                        bool(not bool(Schedule().check_time()) and op_mode == 'Time Control'),
                        #non-emergency, I've reached the desired heat
                        not safety_flag and water_temp > safety_temp,
                        #emergency, I've heated to 10 degrees above the safety temperature
                        water_temp > safety_temp + 10 and safety_flag
                ]
                logger.debug("op_mode_off: {}, out_of_run_time_window: {}".format(*turn_off_conds))

                cur_num = latest_record.status_numeric if latest_record else 0
                #if the tub is off and meets any 'on' condition write to db to turn it on
                if not bool(cur_num) and bool(any(turn_on_conds)):
                    HotTubSwitch().turn_on_hot_tub()

                #if the tub is on and meets any 'off' condition write to db to turn it off
                if bool(cur_num) and not bool(any(turn_on_conds)) and bool(any(turn_off_conds)):
                    HotTubSwitch().turn_off_hot_tub()

                #check the database and execute the relay
                self.switch_tub(latest_record=latest_record)
            except ConnectionResetError:
                pass
        else:
            logger.error("Box temp reached {} degrees f, a dangerous level, shutting down controller at {}".format(box_temp, datetime.now(timezone('America/Los_Angeles'))))
            logger.error("Box will auto-restart at midnight when the circuit cycles")

if __name__ == '__main__':
    #start a redis worker to the name 'hot_tub'
    RelayController().redis_server()
