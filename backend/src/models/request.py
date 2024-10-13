from src import db

class Request(db.model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    veternarian_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    caretaker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.enum('pending', 'completed', 'rejected'), default='pending')
    description = db.Column(db.Text, nullable=False)
    
    veterinarian = db.relationship('User', backref='requests', lazy=True)
    animal = db.relationship('Animal', backref='requests', lazy=True)
    caretaker = db.relationship('User', backref='requests', lazy=True)
    
    def __repr__(self):
        return f'<Request for Animal ID {self.animal_id}>'