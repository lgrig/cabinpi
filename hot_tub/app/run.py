from redis import Redis
from multiprocessing import Process
from queue import Queue
from time import sleep
import rq
class BackgroundTask:
    def __init__(self):
        self.off = False

    def run(self):
        proc = Process(target=self.turn_on)
        proc.start()
        while True:
            #stupid simple polling
            sleep(5)
            if bool(self.off):
                proc.join()

    def turn_on(self):
        queue = rq.Queue('hot_tub_tasks', connection=Redis.from_url('redis://'))
        return queue.enqueue('app.tasks.turn_on_tub', 'self')
