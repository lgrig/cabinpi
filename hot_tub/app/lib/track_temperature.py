from datetime import datetime, timedelta
from app import db
from app.models import WaterTemp, BoxTemp
from app.lib.admin.google_jobs import GoogleJobs
from app.lib.admin import rpi_job
logger = rpi_job.logger

class TrackTemperature:
    def __init__(self):
        self.goog = GoogleJobs()

    def get_records(self):
        #note: these should occur at the same time
        lookback = datetime.now() - timedelta(days=5)
        safety_temp = self.goog.get_safety_temp()
        water_records = db.session.execute("""SELECT * FROM water_temp WHERE create_datetime > '{}' ORDER BY create_datetime DESC""".format(lookback))
        box_records = db.session.execute("""SELECT * FROM box_temp WHERE create_datetime > '{}' ORDER BY create_datetime DESC""".format(lookback))
        #convert records to dictionaries to match times
        box_dict = {box['create_datetime']: box['temperature_f'] for box in box_records}
        record_dict = {water['create_datetime']: {'water': water['temperature_f'], 'box': box_dict[water['create_datetime']] if water['create_datetime'] in box_dict.keys() else None} for water in water_records}
        headers = ['Water Temp', 'Box Temp', 'Safety Temp', 'DateTime']
        records = sorted([[v['water'], v['box'], safety_temp, k] for k, v in record_dict.items()], key=lambda x: x[3], reverse=True)
        records = [headers] + records
        logger.info(records[:3])
        self.goog.write_graph_data(records)

if __name__ == '__main__':
    TrackTemperature().get_records()
