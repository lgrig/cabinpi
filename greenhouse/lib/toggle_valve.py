from datetime import datetime
import pytz
from tools.connection import Connection
"""Class made to Open or Close a valve.
This will be used to control a drip-line irrigation system.
Nice to haves: 
    System should fail closed, don't create a neighborhood leak/drown the plants over bad code/power outages
"""
class ToggleValve():
    def __init__(self):
        self.toggle()

    @staticmethod
    def toggle(position=None):
        """Takes a mandatory keyword argument position which tells it to toggle the valve open or closed"""
        now = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone("US/Pacific")).strftime("%Y-%m-%d %H:%M:%S")
        try:
            """Insert code here to tell the raspberry pi to toggle the valve"""
            pass
            return {
                'timestamp': now,
                'position': position,
                'status': 'success'
            }
        except BaseException as err:
            payload = {
                'timestamp': now,
                'position': position,
                'status': 'failure'
            }
            Connection().send_twilio_sms(msg="ToggleValve Failure with output {}".format(str(payload)))
            return 

if __name__ == '__main__':
    ToggleValve()
