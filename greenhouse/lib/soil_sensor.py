from datetime import datetime
import pytz
from tools.connection import Connection
from Adafruit_MCP3008 import MCP3008


# Software SPI configuration:
# CLK  = 18
# MISO = 23
# MOSI = 24
# CS   = 25
# mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#mcp = MCP3008(spi=SPI.SpiDev(SPI_PORT=0, SPI_DEVICE=0))
#MCP3008.read_adc(5)

class SoilSensor():
    """Reads the soil moisture level and returns it as a dictionary"""
    def __init__(self):
        pass

    @staticmethod
    def measure():
        """Read the soil moisture level and return it as a dictionary"""
        now = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone("US/Pacific")).strftime("%Y-%m-%d %H:%M:%S")
        try:
            moisture_content = None
            return {
                'soil_sensor': {
                    'task': 'soil_sensor',
                    'status': 'success',
                    'value_numeric': moisture_content,
                    'value_enum': None,
                    'timestamp': now}
                }
        except BaseException as err:
            return {
                'soil_sensor': {
                    'task': 'soil_sensor',
                    'status': 'failure',
                    'value_numeric': None,
                    'value_enum': None,
                    'timestamp': now}
                }

if __name__ == '__main__':
    SoilSensor().measure()
