from src.models import WalkingSchedule, Animal, User
from src.repository import Repository

class CaretakerUseCase:
    
    def __init__(self):
        self.schedule_repository = Repository(WalkingSchedule)
        self.animal_repository = Repository(Animal)
        self.user_repository = Repository(User)
    
    def create_animal(self, name: str, species: str, age: int = None, photo: str = None, history: str = None, caretaker_id: int = None) -> Animal:
        new_animal = Animal(
            name=name,
            species=species,
            age=age,
            photo=photo,
            history=history,
            status='available',  # predpokladaný predvolený status
            caretaker_id=caretaker_id
        )
        
        self.animal_repository.add(new_animal)
        return new_animal
    
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
        
        
    def create_request(self, animal_id: int, caretaker_id: int):
        animal = self.animal_repository.get_by_id(animal_id)
        if animal is None:
            raise Exception('Animal not found.')
        animal.status = 'requested'
        animal.caretaker_id = caretaker_id
        self.animal_repository.update(animal)
            
            
    
    
    
    
        
        
        
        
        
        
         
        
    