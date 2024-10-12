from backend import db

class WalkingSchedule(db.Model):
    __tablename__ = 'walking_schedules'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    volunteer = db.relationship('User', backref='walking_schedules', lazy=True)
    status = db.Column(db.String(20))

    def __repr__(self):
        return f'<WalkingSchedule for Animal ID {self.animal_id}>'