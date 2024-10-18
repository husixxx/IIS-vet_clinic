from typing import TypeVar, Generic, List, Type, Optional
from src import db
from ..models import WalkingSchedule, MedicalRecord, Animal
from .tools import to_dict
import base64
import logging

class PublicRepository():
    def __init__(self):
        self.db_session = db.session
    def get_animal_info(self, animal_id: int):
        
        animal = db.session.query(Animal).filter(
            Animal.id == animal_id
        ).first()
        
        if not animal:
            raise ValueError("Animal with this id does not exist")
        
        schedules = db.session.query(WalkingSchedule).filter(
            WalkingSchedule.animal_id == animal_id
        ).all()
           
        medical_records = db.session.query(MedicalRecord).filter(
            MedicalRecord.animal_id == animal_id
        ).all()
        
        if animal.photo:
            photo_base64 = base64.b64encode(animal.photo).decode('utf-8')
        else:
            photo_base64 = None

        
        return {
            "animal": {
                "id": animal.id,
                "name": animal.name,
                "breed": animal.breed,
                "age": animal.age,
                "photo": photo_base64,  # Vrátí Base64 kódovaný obrázek
                "history": animal.history,
                "description": animal.description,
                "sex": animal.sex
            },
            "schedules": [to_dict(schedule) for schedule in schedules],
            "medical_records": [to_dict(record) for record in medical_records]
        }
        
    def check_reservation(self, animal_id: int,start_time: str, end_time: str):
        
        schedule = self.db_session.query(WalkingSchedule).filter(
            WalkingSchedule.animal_id == animal_id,
            WalkingSchedule.start_time == start_time,
            WalkingSchedule.end_time == end_time
        ).first()
        
        if not schedule:
            raise ValueError("No schedule found")
        
        if schedule:
            return to_dict(schedule)
    
    def filter_animals(self, name: str, age: int, breed: str, date: str):
        animals = self.db_session.query(Animal)
       
        if name:
            animals = animals.filter(Animal.name == name)
        
        if age is not None:
            animals = animals.filter(Animal.age == age)
            
        if breed:
            animals = animals.filter(Animal.breed == breed)
        
        animals = animals.all()
        
        if not animals:
            raise ValueError("No animals found")
        
        return [to_dict(animal) for animal in animals]
        
    
        