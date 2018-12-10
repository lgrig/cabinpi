from app import models
from app.lib import rpi_job
from app.lib.run_time import RunTime
from app.lib.relay_switch import RelaySwitch
from datetime import datetime

class Controller(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()

    def switch_tub(self, current_state, relay):
        if current_state.status_numeric == 1 and relay:
            relay.on()
        if current_state.status_numeric == 0 and relay:
            relay.off()

    def redis_server(self, gpio_pin=None):
        relay = gpiozero.LED(18) if self.is_rpi else None
        while True:
            operation_mode = self.get_operation_type()
            safety_temp = self.get_safety_temp()
            current_temp = models.WaterTemp.query.order_by(models.WaterTemp.id.desc()).first()
            current_state = models.GPIOTask.query.order_by(models.GPIOTask.id.desc()).first()
            turn_on_conditions = [safety_temp > current_temp, operation_mode == 'Turn On', bool(RunTime().check_time())] 
            turn_off_conditions = [operation_mode == 'Turn Off', not bool(RunTime().check_time())]
            if current_state.status_numeric == 0:
                if bool(any(turn_on_conditions)):
                    RelaySwitch().turn_on_hot_tub()
                continue
            else:
                if bool(any(turn_off_conditions)):
                    RelaySwitch().turn_off_hot_tub()
                continue 

            self.switch_tub(current_state=current_state, relay=relay)

if __name__ == '__main__':
    #start a redis worker to the name 'hot_tub'
    Controller().redis_server()
