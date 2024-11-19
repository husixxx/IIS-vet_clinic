from src.models import User, Animal, Reservation, WalkingSchedule
from src.repository import Repository, PublicRepository
from datetime import datetime


"""
Use case class handling volunteer-related operations.

Attributes:
    reservation_repository (Repository): Repository for handling Reservation entities
    public_repository (PublicRepository): Repository for complex operations
    animal_repository (Repository): Repository for handling Animal entities

Methods:
    create_reservation: Creates a new reservation for a volunteer to spend time with an animal
    delete_reservation: Deletes an existing pending reservation
    get_history: Retrieves reservation history for a specific volunteer by id
"""


class VolunteerUseCase:
    def __init__(self):
        self.reservation_repository = Repository(Reservation)
        self.public_repository = PublicRepository()
        self.animal_repository = Repository(Animal)

    def create_reservation(
        self, volunteer_id: int, animal_id: int, start_time: str, end_time: str
    ) -> None:
        animal = self.animal_repository.get_by_id(animal_id)
        if not animal:
            raise ValueError("Animal with this id does not exist")

        start_time_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        schedule = self.public_repository.check_reservation(
            animal_id, start_time, end_time
        )

        if not schedule:
            raise ValueError("This time is not available")

        new_reservation = Reservation(
            animal_id=animal_id,
            volunteer_id=volunteer_id,
            start_time=start_time_dt,
            end_time=end_time_dt,
            status="pending",
        )

        self.reservation_repository.add(new_reservation)

    def delete_reservation(self, reservation_id: int) -> None:
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            raise ValueError("Reservation with this id does not exist")
        if reservation.status != "pending":
            raise ValueError("Reservation can't be deleted")
        self.reservation_repository.delete(reservation)

    def get_history(self, volunteer_id: int):
        return self.public_repository.get_all_reservations_by_volunteer_id(volunteer_id)
