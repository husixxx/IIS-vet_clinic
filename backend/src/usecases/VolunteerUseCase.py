from src.models import User, Animal, Reservation, WalkingSchedule
from src.repository import Repository, PublicRepository
from datetime import datetime

class VolunteerUseCase:
    def __init__(self):
        self.reservation_repository = Repository(Reservation)
        self.public_repository = PublicRepository()
        self.animal_repository = Repository(Animal)

    def create_reservation(self, volunteer_id: int, animal_id: int, start_time: str, end_time: str) -> None:
        animal = self.animal_repository.get_by_id(animal_id)
        if(not animal):
            raise ValueError("Animal with this id does not exist")
        
        start_time_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        
        schedule = self.public_repository.check_reservation(animal_id, start_time, end_time)
        
        if not schedule:
            raise ValueError("This time is not available")
        
        new_reservation = Reservation(
            animal_id=animal_id,
            volunteer_id=volunteer_id,
            start_time=start_time_dt,
            end_time=end_time_dt,
            status='pending'
        )
        
        self.reservation_repository.add(new_reservation)
        
    def delete_reservation(self, reservation_id: int) -> None:
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            raise ValueError("Reservation with this id does not exist")
        if reservation.status != 'pending':
            raise ValueError("Reservation can't be deleted")
        self.reservation_repository.delete(reservation)
    
    def get_history(self, volunteer_id: int):
        reservations = self.reservation_repository.get_all()
        return [reservation for reservation in reservations if reservation.volunteer_id == volunteer_id]