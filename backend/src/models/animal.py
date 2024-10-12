from src import db

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    photo = db.Column(db.Text)
    history = db.Column(db.Text)
    medical_records = db.relationship('MedicalRecord', backref='animal', lazy=True)
    status = db.Column(db.String(50))
    caretaker_id = db.Column(db.Integer, db.ForeignKey('users.id'))  
    caretaker = db.relationship('User', backref='animals', lazy=True) 
    
    def __repr__(self):
        return f'<Animal {self.name} ({self.species})>'