from app import db

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
