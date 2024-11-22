from src.models import WalkingSchedule, Animal, User, Request, Reservation
from src.repository import Repository, PublicRepository


"""
Use case class handling caretaker-related operations for animals management.

Attributes:
    schedule_repository (Repository): Repository for handling WalkingSchedule entities
    animal_repository (Repository): Repository for handling Animal entities
    user_repository (Repository): Repository for handling User entities
    request_repository (Repository): Repository for handling Request entities
    reservation_repository (Repository): Repository for handling Reservation entities
    public_repository (PublicRepository): Repository for complex public operations

Methods:
    create_animal: Creates a new animal record
    create_walking_schedule: Creates a new walking schedule for an animal
    verify_volunteer: Verifies a volunteers status
    get_all_animals: Retrieves all animals in the system
    get_all_schedules: Retrieves all walking schedules
    remove_animal: Removes an animal from the system
    get_all_veterinarians: Retrieves all veterinarians
    create_vet_request: Creates a new veterinary request
    get_all_unverified_volunteers: Retrieves all unverified volunteers
    accept_reservation: Accepts a volunteers reservation request
    decline_reservation: Declines a volunteers reservation request
    get_all_reservations: Retrieves all reservations
    get_all_vet_requests: Retrieves all veterinary requests
    cancel_vet_request: Cancels a veterinary request
    filter_animals: Filters animals based on given parameters
    change_reservation_status: Updates the status of a reservation
    delete_animal: Deletes an animal
"""


class CaretakerUseCase:

    def __init__(self):
        self.schedule_repository = Repository(WalkingSchedule)
        self.animal_repository = Repository(Animal)
        self.user_repository = Repository(User)
        self.request_repository = Repository(Request)
        self.reservation_repository = Repository(Reservation)
        self.public_repository = PublicRepository()

    ### Delete Animal ###
    def delete_animal(self, animal_id: int):
        animal = self.animal_repository.get_by_id(animal_id)

        if not animal:
            raise ValueError("Animal not found, hahaha, id == ", animal_id)
        
        self.public_repository.delete_animal(animal_id)


    ### Create Animal ###
    def create_animal(
        self,
        name: str,
        breed: str,
        age: int,
        photo: bytes,
        history: str,
        description: str,
        sex: str,
    ) -> Animal:

        if (
            name == None
            or breed == None
            or age == None
            or history == None
            or description == None
            or sex == None
        ):
            raise ValueError("Missing fields")

        new_animal = Animal(
            name=name,
            breed=breed,
            age=age,
            photo=photo,
            history=history,
            description=description,
            sex=sex,
        )
        self.animal_repository.add(new_animal)
        return new_animal

    ### Create Walking Schedule ###
    def create_walking_schedule(
        self, animal_id: int, start_time: str, end_time: str
    ) -> WalkingSchedule:
        
        if not self.animal_repository.get_by_id(animal_id):
            raise Exception("Animal not found.")
        
        walking_schedule = WalkingSchedule(
            animal_id=animal_id,
            start_time=start_time,
            end_time=end_time,
        )

        self.schedule_repository.add(walking_schedule)
        return walking_schedule
    
    def update_walking_schedule(self, walking_shcedule_id: int, start_time: str, end_time: str):
        
        walking_schedule = self.schedule_repository.get_by_id(walking_shcedule_id)

        if not walking_schedule:
            raise ValueError("Walking schedule not found")
        
        walking_schedule.start_time = start_time
        walking_schedule.end_time = end_time
        self.schedule_repository.update(walking_schedule)

    def update_animal(self, animal_id: int, name: str, breed: str, age: int, history: str, description: str, sex: str):
        
        animal = self.animal_repository.get_by_id(animal_id)

        if not animal:
            raise ValueError("Animal not found")
        
        animal.name = name
        animal.breed = breed
        animal.age = age
        animal.history = history
        animal.description = description
        animal.sex = sex
        self.animal_repository.update(animal)

    
    def verify_volunteer(self, id: int) -> User:
        volunteer = self.user_repository.get_by_id(id)
        if volunteer is None:
            raise Exception("User not found.")
        if volunteer.role_id != 5:
            raise Exception("User is verified.")
        volunteer.verified = True
        volunteer.role_id = 1
        self.user_repository.update(volunteer)
        return volunteer
    
    def unverify_volunteer(self, id: int) -> User:
        volunteer = self.user_repository.get_by_id(id)
        if volunteer is None:
            raise Exception("User not found.")
        if volunteer.role_id != 1:
            raise Exception("User is not a volunteer.")
        volunteer.verified = False
        volunteer.role_id = 5
        self.user_repository.update(volunteer)
        return volunteer

    ### Get All Animals ###
    def get_all_animals(self) -> list:
        return self.animal_repository.get_all()

    ### Get All Schedules ###
    def get_all_schedules(self) -> list:
        return self.schedule_repository.get_all()

    ### Remove Animal ###
    def remove_animal(self, animal_id: int):
        animal = self.animal_repository.get_by_id(animal_id)
        if animal is None:
            raise Exception("Animal not found.")
        try:
            self.animal_repository.delete(animal)
        except:
            raise Exception("Animal has walking schedules.")

    ### Get All Veterinarians ###
    def get_all_veterinarians(self) -> list:
        return self.user_repository.model.query.filter_by(role_id=2).all()

    ### Create request for veterinarian ###
    def create_vet_request(
        self,
        animal_id: int,
        veterinarian_username: str,
        request_date: str,
        description: str,
    ):

        veterinarian = self.public_repository.get_by_username(veterinarian_username)
        animal = self.animal_repository.get_by_id(animal_id)
        
        if animal is None:
            raise Exception("Animal not found.")
        if veterinarian is None or veterinarian.role_id != 2:
            raise Exception("Veterinarian not found.")
        
        new_request = Request(
            animal_id=animal_id,
            veterinarian_id=veterinarian.id,
            request_date=request_date,
            description=description,
            status="pending",
        )

        self.request_repository.add(new_request)
        return new_request

    ### Get all volunteers to verify ###
    def get_all_unverified_volunteers(self) -> list:
        return self.public_repository.get_unverified_volunteers()

    ### Accept volunteer reservation request ###
    def accept_reservation(self, request_id: int):
        request = self.reservation_repository.get_by_id(request_id)
        if request is None:
            raise Exception("reservation not found.")
        request.accepted = True
        self.reservation_repository.update(request)
        return request

    ### Decline volunteer reservation request ###
    def decline_reservation(self, request_id: int):
        request = self.reservation_repository.get_by_id(request_id)
        if request is None:
            raise Exception("reservation not found.")
        request.accepted = False
        self.reservation_repository.update(request)
        return request

    ### Get all reservations to handle ###
    def get_all_reservations(self) -> list:
        return self.reservation_repository.get_all()

    ### Get all vet requests ###
    def get_all_vet_requests(self) -> list:
        return self.request_repository.get_all()

    def cancel_vet_request(self, vet_request_id):
        vet_request = self.request_repository.get_by_id(vet_request_id)
        if vet_request is None:
            raise Exception("vet_request not found")
        vet_request.status = "cancelled"
        self.reservation_repository.update(vet_request)
        return vet_request

    def filter_animals(self, name: str, age: int, breed: str, availability) -> list:
        return self.public_repository.filter_animals(name, age, breed, availability)

    def change_reservation_status(self, reservation_id: int, status: str):
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if reservation is None:
            raise Exception("No reservation")
        if status not in ["pending", "approved", "cancelled", "completed"]:
            raise ValueError("Invalid status")
        reservation.status = status
        self.reservation_repository.update(reservation)
        return reservation
