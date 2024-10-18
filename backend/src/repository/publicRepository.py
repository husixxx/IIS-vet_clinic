from typing import TypeVar, Generic, List, Type, Optional
from src import db
from ..models import WalkingSchedule, MedicalRecord, Animal
from .tools import to_dict
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
                
        return {
            "animal": to_dict(animal),
            "schedules": [to_dict(schedule) for schedule in schedules],
            "medical_records": [to_dict(record) for record in medical_records]
        }
        
    def check_reservation(self, animal_id: int,start_time: str, end_time: str):
        
        schedule = self.db_session.query(WalkingSchedule).filter(
            WalkingSchedule.animal_id == animal_id,
            WalkingSchedule.start_time == end_time,
            WalkingSchedule.end_time == start_time
        ).first()
        
        if not schedule:
            raise ValueError("No schedule found")
        
        if schedule:
            return to_dict(schedule)
    
    def filter_animals(self, animal_type: str, breed: str, age: int):
        animals = db.session.query(Animal).filter(
            Animal.animal_type == animal_type,
            Animal.breed == breed,
            Animal.age == age
        ).all()
        
        if not animals:
            raise ValueError("No animals found")
        
        return [to_dict(animal) for animal in animals]