import sys
from flask_login import LoginManager

sys.path.append('/home/pi/development/python/cabinpi/hot_tub/')
sys.path.append('/home/pi/development/python/cabinpi/hot_tub/app')

from flask import Flask
from flask_login import UserMixin

from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)
login = LoginManager(app)

from app import routes, models
