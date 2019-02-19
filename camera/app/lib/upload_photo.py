import os
from threading import Thread
import dropbox
from app.lib.cabin_camera import CabinCamera
from app.lib.config import Config
from app.lib.logger import Logger
logger = Logger("cabin_camera").get_logger()

class UploadPhoto(CabinCamera):
    def __init__(self):
        pass

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
