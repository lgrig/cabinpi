import logging
import os

loggers = {}
class Logger:
    def __init__(self):
        pass

    def get_logger(self):
        if loggers.get('hot_tub'):
            return loggers.get('hot_tub')
        logger = logging.getLogger('hot_tub')
        logger.setLevel(logging.INFO)

        fh = logging.FileHandler(os.path.dirname(os.path.realpath(__file__)) + '/hot_tub.log')
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        loggers['hot_tub'] = logger

        return logger
