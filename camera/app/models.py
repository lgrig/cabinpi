from app import db

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    create_datetime = db.Column(db.DateTime)
