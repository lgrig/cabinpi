from lib import rpi_job
from app import db
from app.models import RunTime
from sqlalchemy.orm import sessionmaker

class Schedule(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()

    def truncate_existing_time_schedule(self):
        db.session.execute('''TRUNCATE TABLE run_time''')
        db.session.commit()
        db.session.close()

    def repopulate_existing_time_schedule(self):
        schedules = self.get_times()
        for sched in schedules:
            db.session.add(RunTime(start_time=sched[0], end_time=sched[1]))
            db.session.commit()
