from src import db

class WalkingSchedule(db.Model):
    __tablename__ = 'walking_schedules'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    reservated = db.Column(db.Boolean, nullable=False, default=False)
    def __repr__(self):
        return f'<WalkingSchedule for Animal ID {self.animal_id}>'
