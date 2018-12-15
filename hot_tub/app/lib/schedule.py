from datetime import datetime
from pytz import timezone
from app.models import RunTime
from app.lib.google_jobs import GoogleJobs
from app import db, models
from app.lib import rpi_job
logger = rpi_job.logger

goog = GoogleJobs()
class Schedule(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()

    def refresh_times(self):
        times = goog.get_times()
        if not times:
            return
        db.session.execute("DELETE FROM run_time;")
        db.session.commit()

        for time in times:
            db.session.add(RunTime(**{'start_time': time[0], 'end_time': time[1]}))
            db.session.commit()
        return times

    def check_time(self):
        times = models.RunTime.query.all()
        now_time = datetime.now(timezone('America/Los_Angeles')).time()
        for time in times:
            if now_time > time.start_time and now_time < time.end_time:
                return True
        return False
if __name__ == '__main__':
    sched = Schedule()
    sched.refresh_times()
    sched.check_time()
