from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
        return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<user {}>'.format(self.username)

    def set_password(self, password):
                self.password_hash = generate_password_hash(password)

    def check_password(self, password):
                return check_password_hash(self.password_hash, password)

class GPIOTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    status_enum = db.Column(db.String(128))
    status_numeric = db.Column(db.Integer)
    description = db.Column(db.String(500))
    create_datetime = db.Column(db.DateTime)

class RunTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, index=True)
    end_time = db.Column(db.Time, index=True)

class WaterTemp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature_f = db.Column(db.Float(precision=2, asdecimal=True))
    create_datetime = db.Column(db.DateTime)

class BoxTemp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature_f = db.Column(db.Float(precision=2, asdecimal=True))
    create_datetime = db.Column(db.DateTime)
