"""Server to run on a redis worker and poll internal db for changes.
   If changes are found, execute scripts.
"""
from datetime import time
import gpiozero
from app import models
from app.lib import rpi_job
from app.lib.run_time import RunTime
from app.lib.relay_switch import RelaySwitch
from app.lib.google_jobs import GoogleJobs
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
        cur_num = latest_record.status_numeric
        return self.relay.on() if bool(cur_num) else self.relay.off()

    def redis_server(self):
        """Server to watch for relevant databse changes"""
        while True:
            #poll these less frequently, they require a google sheets server check
            op_mode, safety_temp, laps = goog.get_operation_type(), goog.get_safety_temp(), 0
            while laps < 60:
                current_temp = models.WaterTemp.query.order_by(models.WaterTemp.id.desc()).first()
                latest_record = models.GPIOTask.query.order_by(models.GPIOTask.id.desc()).first()
                turn_on_conds = [safety_temp > current_temp, op_mode == 'Turn On', bool(RunTime().check_time())]
                turn_off_conds = [op_mode == 'Turn Off', not bool(RunTime().check_time())]
                cur_num = latest_record.status_numeric
                #if the tub is off and meets any 'on' condition write to db to turn it on
                if not bool(cur_num) and bool(any(turn_on_conds)):
                    RelaySwitch().turn_on_hot_tub()

                #if the tub is on and meets any 'off' condition write to db to turn it off
                if bool(cur_num) and not (safety_temp > current_temp) and bool(any(turn_off_conds)):
                    RelaySwitch().turn_off_hot_tub()

                #check the database and execute the relay
                self.switch_tub(latest_record=latest_record)
                time.sleep(1)
                laps += 1

if __name__ == '__main__':
    #start a redis worker to the name 'hot_tub'
    RelayController().redis_server()
