from . import db
from .animal import Animal

class Caretaker(db.Model):
    __tablename__ = 'caretakers'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    managed_animals = db.relationship('Animal', backref='caretaker', lazy=True)

    def __repr__(self):
        return f'<Caretaker ID {self.id}>'