from src import db

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('pending','approved','completed', default='pending', name='reservation_status'))
    
    
    volunteer = db.relationship('User', backref='reservations', lazy=True)
    animal = db.relationship('Animal', backref='reservations', lazy=True)
    
    def __repr__(self):
        return f'<Reservation for Animal ID {self.animal_id}>'
    