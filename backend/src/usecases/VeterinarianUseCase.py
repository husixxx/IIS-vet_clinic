from src.models import Request, MedicalRecord
from src.repository import Repository, PublicRepository


class VeterinarianUseCase:
    def __init__(self):
        self.request_repository = Repository(Request)
        self.public_repository = PublicRepository()
        self.medical_record_repository = Repository(MedicalRecord)

    def get_all_requests_by_vet_id(self, vet_id: int):
        return self.public_repository.get_all_vet_requests(vet_id)

    def schedule_request(self, request_id: int, date_time: str, status: str) -> Request:
        request = self.request_repository.get_by_id(request_id)
        if not request:
            raise ValueError("Request with this id does not exist")
        if status not in ["scheduled", "completed", "cancelled", "pending"]:
            raise ValueError("Invalid status")
        request.status = status
        request.request_date = date_time
        self.request_repository.update(request)
        return request

    def create_medical_record(
        self,
        animal_id: int,
        examination_date: str,
        description: str,
        examination_type: str,
        vet_id: int,
    ) -> MedicalRecord:

        new_medical_record = MedicalRecord(
            animal_id=animal_id,
            examination_date=examination_date,
            description=description,
            examination_type=examination_type,
            veterinarian_id=vet_id,
        )
        # self.public_repository.add(new_medical_record)
        self.medical_record_repository.add(new_medical_record)
        return new_medical_record
    
    def update_medical_record(self, medical_record_id: int, veterinarian_id: int, examination_date: str, examination_type: str, description: str):
        
        medical_record = self.medical_record_repository.get_by_id(medical_record_id)

        if not medical_record:
            raise ValueError("Medical record not found")
        
        if int(medical_record.veterinarian_id) != int(veterinarian_id):
            raise ValueError("You can modify only your medical records")
        
        medical_record.examination_date = examination_date
        medical_record.examination_type = examination_type
        medical_record.description = description
        self.medical_record_repository.update(medical_record)

        
        
        
