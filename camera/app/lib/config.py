import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development_secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    is_rpi = 'arm' in os.uname()[4][:3]
    if is_rpi:
        CREDS_PATH = '/home/pi/development/.credentials.json'
        CONFIG_PATH = ''
    else:
        CREDS_PATH = '/Users/Grignon/development/.credentials.json'
        CONFIG_PATH = '/Users/Grignon/development/.config.json'

    config = json.loads(open(CONFIG_PATH).read())

    def __init__(self):
        super().__init__()
