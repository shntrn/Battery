from batteryapp import db
from datetime import datetime


class Battery(db.Model):
    battery_id = db.Column(db.Integer, primary_key=True)
    battery_num = db.Column(db.Integer, index=True, unique=True)
    status_ref = db.Column(db.Integer, db.ForeignKey('status.status_id'))
    battery_log = db.relationship('Batterylog', backref='battery')
    room = db.Column(db.String(32), default='310')
    capacity = db.Column(db.Integer)
    last_update = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Battery {self.battery_num}>'

class Batterylog(db.Model):
    history_id = db.Column(db.Integer, primary_key=True)
    battery_ref = db.Column(db.Integer, db.ForeignKey('battery.battery_id'))
    status_ref = db.Column(db.Integer, db.ForeignKey('status.status_id'))
    room = db.Column(db.String(32), default='310')
    capacity = db.Column(db.Integer)
    last_update = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<room {self.room} capacity {self.capacity}, last_update {self.last_update}>'

class Status(db.Model):
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(20))

    def __repr__(self):
        return f'<Status {self.status_name}'








