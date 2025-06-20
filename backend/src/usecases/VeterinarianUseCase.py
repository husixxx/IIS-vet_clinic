from src.models import Request, MedicalRecord, Animal, User
from src.repository import Repository, PublicRepository
from datetime import datetime


class VeterinarianUseCase:
    def __init__(self):
        self.animal_repository = Repository(Animal)
        self.user_repository = Repository(User)
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
        datetime_dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        if datetime_dt < datetime.now():
            raise ValueError("Date cannot be in the past")
        
        if status == "scheduled" and request.status != "pending":
            
            raise ValueError("Can only schedule pending requests")
            
        if status == "completed" and request.status != "scheduled":
            raise ValueError("Can only complete scheduled requests")
            
        if status == "cancelled" and request.status not in ["pending", "scheduled"]:
            raise ValueError("Can only cancel pending or scheduled requests")
            
        if request.status in ["cancelled", "completed"]:
            raise ValueError("Cannot modify cancelled or completed requests")

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

        vet = self.user_repository.get_by_id(vet_id)
        if not vet:
            raise ValueError("Veterinarian not found")
        if vet.role_id != 2:
            raise ValueError("User is not a veterinarian")

        animal = self.animal_repository.get_by_id(animal_id)
        if not animal:
            raise ValueError("Animal not found")
        datetime_dt = datetime.strptime(examination_date, "%Y-%m-%d")
        if datetime_dt > datetime.now():
            raise ValueError("Examination date cannot be in the future")

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

    def update_medical_record(
        self,
        medical_record_id: int,
        veterinarian_id: int,
        examination_date: str,
        examination_type: str,
        description: str,
    ):

        medical_record = self.medical_record_repository.get_by_id(medical_record_id)

        if not medical_record:
            raise ValueError("Medical record not found")

        if int(medical_record.veterinarian_id) != int(veterinarian_id):
            raise ValueError("You can modify only your medical records")

        medical_record.examination_date = examination_date
        medical_record.examination_type = examination_type
        medical_record.description = description
        self.medical_record_repository.update(medical_record)
        return medical_record
