"""
    Connector to pygsheets for hot tub controls.
    Application only attempts to ping the hot_tub database every minute.
"""
import pygsheets
from datetime import datetime
from app.lib.config import Config
from app.lib import rpi_job
logger = rpi_job.logger

class GoogleJobs(rpi_job.RPIJob):
    def __init__(self):
        super().__init__()
        self.ctrl = self.get_hot_tub_controller()

    def get_hot_tub_controller(self):
        pyg = pygsheets.authorize(service_file=Config.CREDS_PATH)
        sheet = pyg.open_by_key('1wWj0sFmgwsTRolqUV2fQqFCxxN7kWzHS-FXNtAB1ymk')
        return sheet.worksheet_by_title('Controls')

    def get_times(self):
        """returns a matrix of times of format [[start_time, end_time], [start_time, end_time]]"""
        cells_matrix = self.ctrl.get_named_ranges('run_times').cells
        try:
            vals_matrix = [[datetime.strptime(col.value, '%H:%M').time() for col in row] for row in cells_matrix[1:] if bool(row[0].value)]
        except ValueError:
            logger.info("BAD TIME INPUTS")
            vals_matrix = None
        return vals_matrix if bool(vals_matrix) else None

    def get_safety_temp(self):
        """returns the desired safety temperature in degrees farenheit"""
        return int(self.ctrl.get_named_ranges('safety_temperature').cells[0][0].value)

    def get_operation_type(self):
        """returns tub run status (Turn On, Turn Off, Time Control)"""
        return self.ctrl.get_named_ranges('manual_operation').cells[0][0].value

if __name__ == '__main__':
    logger.info(GoogleJobs().get_operation_type())
    logger.info(GoogleJobs().get_safety_temp())
    logger.info(GoogleJobs().get_times())
