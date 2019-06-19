import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development_secret'

    SQLALCHEMY_DATABASE_URI = os.environ.get('RALSTON_DB_URL') or\
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        super().__init__()

    is_rpi = 'arm' in os.uname()[4][:3]
    if is_rpi:
        CREDS_PATH = '/home/pi/development/.credentials.json'
    else:
        CREDS_PATH = '/Users/Grignon/development/.credentials.json'
