from src.models import Request, MedicalRecord
from src.repository import Repository, PublicRepository

class VeterinarianUseCase:
    def __init__(self):
        self.request_repository = Repository(Request)
        self.public_repository = PublicRepository()

    def get_all_requests_by_vet_id(self, vet_id: int):
        return self.public_repository.get_all_vet_requests(vet_id)
    
    def schedule_request(self, request_id: int, date_time: str):
        request = self.request_repository.get_by_id(request_id)
        if not request:
            raise ValueError("Request with this id does not exist")
        status = 'scheduled'
        request.status = status
        request.request_date = date_time
        self.request_repository.update(request)
        return request
    
    def create_medical_record(self, animal_id: int, examination_date: str, description: str, examination_type: str, vet_id: int) -> MedicalRecord:
        
        new_medical_record = MedicalRecord(
            animal_id=animal_id,
            examination_date=examination_date,
            description=description,
            examination_type=examination_type,
            veterinarian_id=vet_id
        )
        self.public_repository.add(new_medical_record)
        return new_medical_record
        
        
        