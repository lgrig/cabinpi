"""Relay Switch Class: create server to read changes to the database
   If a change is detected, adjust the pin accordingly.
   Start up should take the last pin position and run pins accordingly.
"""
from lib import rpi_job
class RelaySwitch(rpi_job.RPIJob):
    def __init__(self):
        __init__.super()

    def turn_on_hot_tub(self):
        db.session.add(GPIOTask('hot_tub', 'on', 1, 'turn on tub', datetime.now()))
        db.session.commit()

    def turn_off_hot_tub(self):
        """Turn on the relay switch, it will continue to run"""
        db.session.add(GPIOTask('hot_tub', 'off', 0, 'turn off tub', datetime.now()))
        db.session.commit()

    def redis_server(self, gpio_pin=None):
        relay = gpiozero.LED(self.gpio_pin) if self.is_rpi else None
        while True:
            latest = GPIOTask.query.order_by(GPIOTask.id.desc()).first()
            if latest.status_numeric == 1:
                if relay:
                    relay.on()
                else:
                    logger.info("Dev Debug msg: I turned on the hot tub")
            if latest.status_numeric == 0:
                if relay:
                    relay.off()
                else:
                    logger.info("Dev Debug msg: I turned off the hot tub")
            sleep(1)

if __name__ == '__main__':
    #start a redis worker to the name 'hot_tub'
    RelaySwitch().start_worker()
    RelaySwitch().redis_server()
