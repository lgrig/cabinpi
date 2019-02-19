from cv2 import cv2
import numpy as np
from app.lib.cabin_camera import CabinCamera
from app.lib.capture import Capture
class SetAreaOfInterest(CabinCamera):
    """Test image is 100 x 75 pixels, coords are top-left, top-right, bottom-right, bottom-left"""
    def __init__(self, coords=None):
        super().__init__()
        self.tmp_coords = coords or [(0, 75), (100, 75), (100, 0), (0, 0)]

    def build_test_image(self):
        _, img = Capture().capture_test_image()
        img.seek(0)
        img_array = np.asarray(bytearray(img.read()), dtype=np.uint8)
        cv2_img = cv2.imdecode(img_array, 0)
        cv2.rectange(cv2_img, self.coords)
        cv2.imwrite(self.save_path + 'test_img_box.jpg')

    def set_new_coords(self):
        self.coords = self.tmp_coords
