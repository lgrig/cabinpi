import logging
import os

loggers = {}
class Logger:
    def __init__(self, name):
        self.name = name
        self.path = os.path.dirname(os.path.realpath(__file__))

    def get_logger(self):
        if loggers.get(self.name):
            return loggers.get(self.name)
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)

        fh = logging.FileHandler(self.path + '/' + self.name + '.log')
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        loggers[self.name] = logger

        return logger
