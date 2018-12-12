"""
    Connector to pygsheets for hot tub controls.
    Application only attempts to ping the hot_tub database every minute.
"""
import pygsheets
from app.lib.config import Config
class GoogleJobs:
    def __init__(self):
        pass

    def get_hot_tub_controller(self):
        pyg = pygsheets.authorize(service_file=Config.CREDS_PATH)
        sheet = pyg.open_by_key('1wWj0sFmgwsTRolqUV2fQqFCxxN7kWzHS-FXNtAB1ymk')
        return sheet.worksheet_by_title('Controls')

    def get_times(self):
        """returns a matrix of times of format [[start_time, end_time], [start_time, end_time]]"""
        ctrl = self.get_hot_tub_controller()
        vals_matrix = ctrl.get_named_ranges('run_times').data()
        return [val for val in vals_matrix if bool(val[0])]

    def get_safety_temp(self):
        """returns the desired safety temperature in degrees farenheit"""
        ctrl = self.get_hot_tub_controller()
        return ctrl.get_named_ranges('safety_temperature').data()[0][0]

    def get_operation_type(self):
        """returns tub run status (Turn On, Turn Off, Time Control)"""
        ctrl = self.get_hot_tub_controller()
        return ctrl.get_named_ranges('manual_operation').data()[0][0]
