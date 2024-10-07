from . import db
from .animal import Animal

class Veterinarian(db.Model):
    __tablename__ = 'veterinarians'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    treated_animals = db.relationship('MedicalRecord', backref='veterinarian', lazy=True)

    def __repr__(self):
        return f'<Veterinarian ID {self.id}>'