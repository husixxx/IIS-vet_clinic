from src import db

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    veterinarian_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'rejected', default='pending', name='request_status'))
    description = db.Column(db.Text, nullable=False)
    
    veterinarian = db.relationship('User',foreign_keys=[veterinarian_id] ,backref='veterinarians_requests', lazy=True)
    animal = db.relationship('Animal', backref='requests', lazy=True)
    
    def __repr__(self):
        return f'<Request for Animal ID {self.animal_id}>'