from src.models import Animal,MedicalRecord, WalkingSchedule
from src.repository import Repository
from datetime import datetime
from src.repository import PublicRepository

class AnimalUseCase:
    def __init__(self):
        self.public_repository = PublicRepository()

    def get_animal_info_by_id(self, animal_id: int):
        return self.public_repository.get_animal_info(animal_id)
        