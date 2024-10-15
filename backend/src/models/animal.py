from src import db

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    photo = db.Column(db.LargeBinary)
    history = db.Column(db.Text)
    description = db.Column(db.Text)
    medical_records = db.relationship('MedicalRecord', backref='animal', lazy=True)
    sex = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Animal {self.name} ({self.species})>'