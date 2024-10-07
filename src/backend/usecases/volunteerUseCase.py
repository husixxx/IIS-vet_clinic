from backend.models import WalkingSchedule
from backend.repository import Repository

class VolunteerUseCase:
    
    def __init__(self):
        self.schedule_repository = Repository(WalkingSchedule)
    
    def manage_animals(self):
        pass
    
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
        
        
        
        
        
        
         
        
    