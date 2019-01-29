import json
import io
import os
import time
from queue import Queue
from threading import Thread
from datetime import datetime
from PIL import Image
from lib.logger import Logger
from lib.config import Config
import picamera
import dropbox

logger = Logger("cabin_camera").get_logger()
#TO DO!
### SET A LIMIT ON IMAGES UNLESS MAJOR PIXEL CHANGES
### ADD LOGGING FOR NUMBER OF CHANGED PIXELS

# Motion detection settings:
# Threshold (how much a pixel has to change by to be marked as "changed")
# Sensitivity (how many changed pixels before capturing an image)
# ForceCapture (whether to force an image to be captured every forceCaptureTime seconds)
class CabinCamera():
    force_capture = True
    force_capture_time = 3600
    test_width = 100
    test_height = 75
    sensitivity = 0.05 #expressed as fraction of pixels changed
    save_width = 1280
    save_height = 960
    disk_space_to_reserve = 40 * 1024 * 1024 # Keep 40 mb free on disk

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
                    pix_diff = self.check_pixel_difference(buffer1, buffer2)['pix_diff']
                    if pix_diff/(self.test_width*self.test_height) > self.sensitivity:
                        self.capture.capture_full_image()
                    buffer1 = buffer2
            except BaseException as err:
                logger.error("retrying after failure: %s", err)
                retries += 1

    def check_pixel_difference(self, img1=None, img2=None, threshold=None):
        """
        Identifies and counts pixel changes.
        Note: test images are 100 * 75, 7500 pixels, sensitivty is in pixels
        image is currently set to buffer only, need to reset to look at jpgs too.
        Need to build back-testing into this for sensitivity analysis.
        """
        threshold = threshold or 20
        changed_pixels, changed_coords = 0, []
        for x_coord in range(0, self.test_width):
            for y_coord in range(0, self.test_height):
                # [1] corresponds to green channel (highest quality)
                # what are the possible values for changed pixels?
                pixdiff = abs(img1[x_coord, y_coord][1] - img2[x_coord, y_coord][1])
                if pixdiff > threshold:
                    changed_pixels += 1
                    changed_coords.append((x_coord, y_coord))
        return {'pix_diff': changed_pixels, 'changed_coords': changed_coords}

class Capture(CabinCamera):
    save_path = '/home/pi/development/python/cabin_camera/photos/'
    file_fmt = lambda x: "capture-%04d%02d%02d-%02d%02d.jpg" % (x.year, x.month, x.day, x.hour, x.minute)
    def __init__(self):
        super().__init__()
        self.set_camera()
        self.last_capture = None

    def set_camera(self):
        self.camera = picamera.PiCamera()
        self.camera.start_preview()
        self.camera.resolution = (self.test_width, self.test_height)

    def capture_test_image(self):
        """Take a small shitty image to test compare pixels against"""
        stream = io.BytesIO()
        self.camera.capture(stream, format='bmp')
        stream.seek(0)
        img = Image.open(stream)
        buf_out = img.load()
        stream.close()
        return img, buf_out

    def capture_full_image(self):
        """Save full sized image to disk, pass to dbx_upload_worker"""
        file_path = self.save_path + self.file_fmt(datetime.now())
        self.camera.resolution = (self.save_width, self.save_height)
        self.camera.capture(file_path)
        self.q.put(file_path)

        self.set_last_capture()

class UploadPhoto(CabinCamera):
    def __init__(self):
        super().__init__()

    def start_dbx_upload_worker(self):
        """Worker factory"""
        worker = Thread(target=self.upload, args=(self.q,))
        worker.setDaemon(True)
        worker.start()

    def upload(self):
        """Upload files in folder to dropbox"""
        dbx = dropbox.Dropbox(Config.config['dropbox']['token'])
        #while True:
        filepath = self.q.get()
        with open(filepath, 'rb') as dbfile:
            dbx_path = "/photos/" + filepath.split("/")[-1]
            dbx.files_upload(dbfile.read(), dbx_path)
            os.remove(filepath)
        self.q.task_done()
        logger.info("uploaded to dbx: %s", dbx_path)
        return dbx_path

if __name__ == '__main__':
    CabinCamera().run()
