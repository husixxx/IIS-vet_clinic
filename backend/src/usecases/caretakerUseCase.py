from src.models import WalkingSchedule, Animal, User, Request
from src.repository import Repository

class CaretakerUseCase:
    
    def __init__(self):
        self.schedule_repository = Repository(WalkingSchedule)
        self.animal_repository = Repository(Animal)
        self.user_repository = Repository(User)
        self.request_repository = Repository(Request)
    
    ### Create Animal ###
    def create_animal(self, name: str, breed: str, age: int, photo: str, history: str, description: str, sex: str) -> Animal:
        new_animal = Animal(
            name=name,
            breed=breed,
            age=age,
            photo=photo,
            history=history,
            description=description,
            sex=sex
        )
        
        self.animal_repository.add(new_animal)
        return new_animal
    
    ### Create Walking Schedule ###
    def create_walking_schedule(self, animal_id: int, start_time: str, end_time: str) -> WalkingSchedule:
        
        
        walking_schedule = WalkingSchedule(
            animal_id = animal_id,
            start_time = start_time,
            end_time = end_time,
        )
        
        self.schedule_repository.add(walking_schedule)
        return walking_schedule
    
    def verify_volunteer(self, username: str) -> User:
        volunteer = self.user_repository.get_by_username(username)
        if volunteer is None:
            raise Exception('User not found.')
        if volunteer.role_id != 5:
            raise Exception('User is validated.')
        volunteer.verified = True
        volunteer.role_id = 3
        self.user_repository.update(volunteer)
        return volunteer
    
    def get_all_animals(self) -> list:
        return self.animal_repository.get_all()
    
    def get_all_schedules(self) -> list:
        return self.schedule_repository.get_all()
    
    def remove_animal(self, animal_id: int):
        animal = self.animal_repository.get_by_id(animal_id)
        if animal is None:
            raise Exception('Animal not found.')
        try:
            self.animal_repository.delete(animal)
        except:
            raise Exception('Animal has walking schedules.')
        
    def create_vet_request(self, animal_id: int, veterinarian_username: str, request_date: str, description: str):
        
        veterinarian = self.user_repository.get_by_username(veterinarian_username)
        
        if veterinarian is None:
            raise Exception('Veterinarian not found.')        
        new_request = Request(
            animal_id = animal_id,
            veterinarian_id = veterinarian.id,
            request_date = request_date,
            description = description
        )
        
        self.request_repository.add(new_request)
        return new_request
    
    def get_all_unverified_volunteers(self) -> list:
        return self.user_repository.get_unverified_volunteers()
    
            
    
    
    
    
        
        
        
        
        
        
         
        
    