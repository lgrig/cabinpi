from app.models import RunTime
from app.lib.google_jobs import GoogleJobs
from app import db, models
from app.lib import rpi_job
from datetime import datetime
logger = rpi_job.logger

goog = GoogleJobs()
class Schedule(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()

    def refresh_times(self):
        db.session.execute("DELETE FROM run_time;")
        db.session.commit()

        times = goog.get_times()
        for time in times:
            db.session.add(RunTime(**{'start_time': time[0], 'end_time': time[1]}))
            db.session.commit()

    def check_time(self):
        times = models.RunTime.query.all()
        now_time = datetime.now().time()
        for time in times:
            if now_time > time.start_time and now_time < time.end_time:
                logger.info("True")
                return True
        logger.info("False")
        return False
if __name__ == '__main__':
    sched = Schedule()
    sched.refresh_times()
    sched.check_time()
