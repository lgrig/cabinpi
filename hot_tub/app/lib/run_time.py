from app.models import RunTime
from app import db
from app.lib import rpi_job
from datetime import datetime

class RunTime(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()

    def check_time(self):
        times = [u.__dict__ for u in db.session.query(RunTime).all()]
        now_time = datetime.now().time()
        conv_time = lambda x: datetime.strptime(x, "%H:%M:%S")
        for time in times:
            if (now_time > conv_time(time['start_time'])) and (now_time < conv_time(time['end_time'])):
                return True
        return False


