from . import db  

class Person(db.Model):
    __tablename__ = 'persons'  # Název tabulky v databázi
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Person {self.first_name} {self.last_name}>'

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(50), nullable=False)  
    age = db.Column(db.Integer)
    photos = db.Column(db.Text)  # Může obsahovat odkazy na fotky
    history = db.Column(db.Text)  # Informace o nalezení
    medical_records = db.relationship('MedicalRecord', backref='animal', lazy=True)
    status = db.Column(db.String(50))  # Stav (k dispozici, zapůjčené)
    
    def __repr__(self):
        return f'<Animal {self.name} ({self.species})>'

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    examination_date = db.Column(db.Date)
    veterinarian_id = db.Column(db.Integer, db.ForeignKey('veterinarians.id'), nullable=False)
    examination_type = db.Column(db.String(50))  # Očkování, kontrola, léčba
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<MedicalRecord for Animal ID {self.animal_id}>'

class WalkingSchedule(db.Model):
    __tablename__ = 'walking_schedules'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.id'), nullable=False)
    status = db.Column(db.String(20))  # Rezervováno, dokončeno

    def __repr__(self):
        return f'<WalkingSchedule for Animal ID {self.animal_id}>'

class Caretaker(db.Model):
    __tablename__ = 'caretakers'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    managed_animals = db.relationship('Animal', backref='caretaker', lazy=True)

    def __repr__(self):
        return f'<Caretaker ID {self.id}>'

class Veterinarian(db.Model):
    __tablename__ = 'veterinarians'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    treated_animals = db.relationship('MedicalRecord', backref='veterinarian', lazy=True)

    def __repr__(self):
        return f'<Veterinarian ID {self.id}>'

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    is_verified = db.Column(db.Boolean, default=False)
    walking_history = db.relationship('WalkingSchedule', backref='volunteer', lazy=True)

    def __repr__(self):
        return f'<Volunteer ID {self.id}>'
