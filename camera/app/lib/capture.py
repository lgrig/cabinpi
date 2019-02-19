from datetime import datetime
import io
import picamera
from PIL import Image
from app.lib.cabin_camera import CabinCamera

class Capture(CabinCamera):
    capture_fmt = lambda x: "capture-%04d%02d%02d-%02d%02d.jpg" % (x.year, x.month, x.day, x.hour, x.minute)
    video_fmt = lambda x: "video-%04d%02d%02d-%02d%02d.jpg" % (x.year, x.month, x.day, x.hour, x.minute)
    def __init__(self):
        super().__init__()
        self.set_camera()
        self.last_capture = None

    def set_camera(self):
        """Initialization function, starts up the camera and does some basic config"""
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
        file_path = self.save_path + self.capture_fmt(datetime.now())
        self.camera.resolution = (self.save_width, self.save_height)
        self.camera.capture(file_path)
        self.q.put(file_path)
        self.set_last_capture()

    def start_video(self):
        """begin recording video"""
        file_path = self.save_path + self.video_fmt(datetime.now())
        self.camera.start_preview()
        self.camera.start_recording(file_path)

    def stop_video(self):
        """stop recording video"""
        self.camera.stop_recording()
        self.camera.stop_preview()
