from typing import TypeVar, Generic, List, Type, Optional
from src import db
from ..models import WalkingSchedule, MedicalRecord, Animal, Request, Reservation, User
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
    
    def filter_animals(self, name: str, age: int, breed: str, availability: bool = None):
        animals = self.db_session.query(Animal)
       
        if name:
            animals = animals.filter(Animal.name == name)
        
        if age is not None:
            animals = animals.filter(Animal.age == age)
            
        if breed:
            animals = animals.filter(Animal.breed == breed)
        
        approved_reservations = self.db_session.query(Reservation).filter(Reservation.status == 'approved')
        
        if availability is True:
            animals = animals.filter(Animal.id.notin_([reservation.animal_id for reservation in approved_reservations]))
        elif availability is False:
            animals = animals.filter(Animal.id.in_([reservation.animal_id for reservation in approved_reservations]))
        animals = animals.all()
        
        if not animals:
            raise ValueError("No animals found")
        
        return [animal for animal in animals]
    
    
    def get_all_vet_requests(self, vet_id: int):
        requests = self.db_session.query(Request).filter(
            Request.veterinarian_id == vet_id
        ).all()
        
        if not requests:
            raise ValueError("No requests found")
        
        return [request for request in requests]
    

    def get_all_reservations_by_volunteer_id(self, volunteer_id: int):
        reservations = self.db_session.query(Reservation).filter(
            Reservation.volunteer_id == volunteer_id
        ).all()
        
        if not reservations:
            raise ValueError("No requests found")
        
        return [reservation for reservation in reservations]
    
    def get_all_breeds(self):
        breeds = self.db_session.query(Animal.breed).distinct().all()
        
        if not breeds:
            raise ValueError("No breeds found")
        
        return [breed[0] for breed in breeds]
        
    def delete_volunteer(self, volunteer_id: int):
        volunteer = self.db_session.query(User).filter(
            User.id == volunteer_id
        ).first()
        
        if not volunteer:
            raise ValueError("Volunteer not found")
        
        reservations = self.db_session.query(Reservation).filter(
            Reservation.volunteer_id == volunteer_id
        ).all()
        
        for reservation in reservations:
            self.db_session.delete(reservation)
        
        self.db_session.delete(volunteer)
        self.db_session.commit()
    
    def delete_veterinarian(self, vet_id: int):
        vet = self.db_session.query(User).filter(
            User.id == vet_id
        ).first()
        
        if not vet:
            raise ValueError("Veterinarian not found")
        
        requests = self.db_session.query(Request).filter(
            Request.veterinarian_id == vet_id).all()
        
        for request in requests:
            self.db_session.delete(request)
            
        self.db_session.delete(vet)
        self.db_session.commit()
    
    def delete_user(self, user_id: int):
        user = self.db_session.query(User).filter(
            User.id == user_id
        ).first()
        
        if not user:
            raise ValueError("User not found")
        
        self.db_session.delete(user)
        self.db_session.commit()