#import picamera
from datetime import datetime
import os

class Camera():
    """Camera utilities for various photo functions
    takes many kwargs as config options
    save_path='/path/to/saved/photos'
    resolution=(width_integer, height_integer),
    """
    def __init__(self, **kwargs):
        camera = picamera.PiCamera()
        camera.resolution = resolution or (1280, 960)
        self.camera = camera
        self.save_path = save_path or os.path.dirname(os.path.realpath(__file__))

    def take_photo(self):
        now = datetime.now()
        fmt = (now.year, now.month, now.day, now.hour, now.minute)
        filename = "capture-%04d%02d%02d-%02d%02d%02d.jpg" % (fmt)
        try:
            self.camera.capture(self.save_path + filename)
            return {
                'camera': {
                    'task': 'take_photo',
                    'status': 'success',
                    'value_numeric': None,
                    'value_enum': self.save_path + filename,
                    'timestamp': now}
                }

        except BaseException as err:
            return {
                'camera': {
                    'task': 'take_photo',
                    'status': 'failure',
                    'value_numeric': None,
                    'value_enum': None,
                    'timestamp': now}
                }
