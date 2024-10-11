from backend.models import WalkingSchedule, Animal
from backend.repository import Repository

class CaretakerUseCase:
    
    def __init__(self):
        self.schedule_repository = Repository(WalkingSchedule)
        self.animal_repository = Repository(Animal)
    
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
    
    def create_walking_schedule(self, animal_id: int, volunteer_id: int, start_time: str, end_time: str, status: str) -> WalkingSchedule:
        
        walking_schedule = WalkingSchedule(
            animal_id = animal_id,
            volunteer_id = volunteer_id,
            start_time = start_time,
            end_time = end_time,
            status = status
        )
        
        self.schedule_repository.add(walking_schedule)
        return walking_schedule
        
        
        
        
        
        
         
        
    