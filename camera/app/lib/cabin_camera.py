import json
import time
from queue import Queue
from app.lib.logger import Logger
from app.lib.capture import Capture
from app.lib.upload_photo import UploadPhoto

logger = Logger("cabin_camera").get_logger()
# Motion detection settings:
# Threshold (how much a pixel has to change by to be marked as "changed")
# Sensitivity (how many changed pixels before capturing an image)
# ForceCapture (whether to force an image to be captured every forceCaptureTime seconds)
class CabinCamera():
    force_capture = True
    force_capture_time = 3600
    test_width = 100
    test_height = 75
    coords = [None, None, None, None]
    sensitivity = 0.05 #expressed as fraction of pixels changed
    save_width = 1280
    save_height = 960
    disk_space_to_reserve = 40 * 1024 * 1024 # Keep 40 mb free on disk
    save_path = '/home/pi/development/python/cabin_camera/photos/'

    def __init__(self):
        logger.info('starting the Camera')
        #Remote Worker setup
        self.q = Queue()
        self.workers = 1
        self.uploader = UploadPhoto()
        self.capture = Capture()
        self.last_capture = None

    def set_last_capture(self):
        self.last_capture = time.time()

    def run(self):
        logger.info('starting dbx upload worker')
        self.uploader.start_dbx_upload_worker()

        retries = 0
        while retries <= 10:
            try:
                _, buffer1 = self.capture.capture_test_image()
                self.set_last_capture()
                while True:
                    _, buffer2 = self.capture.capture_test_image()
                    list_of_deltas = self.get_deltas(buffer1, buffer2)

                    change_ratio = len(list_of_deltas)/(self.test_width*self.test_height)
                    if change_ratio > self.sensitivity:
                        self.capture.capture_full_image()

                    buffer1 = buffer2
            except BaseException as err:
                logger.error("retrying after failure: %s", err)
                retries += 1

    def get_deltas(self, img1=None, img2=None, threshold=None):
        """
        Identifies and counts pixel changes.
        Note: test images are 100 * 75, 7500 pixels, sensitivty is in pixels
        image is currently set to buffer only, need to reset to look at jpgs too.
        Need to build back-testing into this for sensitivity analysis.
        """
        threshold = threshold or 20
        img_coords = [(x, y) for x in range(0, self.test_width) for y in range(0, self.test_height)]
        #[1] corresponds to green channel (highest quality)
        view_coords = [(x, y) for x in range(self.coords[0], self.coords[1])\
                       for y in range(self.coords[2], self.coords[3])]
        changed_coords = [coord for coord in img_coords if abs(img1[coord][1] - img2[coord][1]) > threshold]
        return list(set(view_coords).intersection(set(changed_coords)))

if __name__ == '__main__':
    CabinCamera().run()
