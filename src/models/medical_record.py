from . import db

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    examination_date = db.Column(db.Date)
    veterinarian_id = db.Column(db.Integer, db.ForeignKey('veterinarians.id'), nullable=False)
    examination_type = db.Column(db.String(50))
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<MedicalRecord for Animal ID {self.animal_id}>'