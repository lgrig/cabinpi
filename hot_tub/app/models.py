from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<user {}>'.format(self.username)

class GPIOTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    status_enum = db.Column(db.String(128))
    status_numeric = db.Column(db.Integer)
    description = db.Column(db.String(500))
    create_time = db.Column(db.DateTime)

