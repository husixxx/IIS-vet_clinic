from . import db
from .walking_schedule import WalkingSchedule

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    is_verified = db.Column(db.Boolean, default=False)
    walking_history = db.relationship('WalkingSchedule', backref='volunteer', lazy=True)

    def __repr__(self):
        return f'<Volunteer ID {self.id}>'