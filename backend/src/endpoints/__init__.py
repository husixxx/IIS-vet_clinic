from flask import Blueprint

# admin
from .Admin.CreateCaretaker import create_caretaker_bp
from .Admin.CreateVeterinarian import create_veterinarian_bp
from .Admin.GetAllUsers import get_all_users_bp
from .Admin import update_user_bp
# caretaker
from .Caretaker.CreateWalkingSchedule import create_walking_schedule_bp
from .Caretaker.CreateAnimal import create_animal_bp
from .Caretaker.VerifyVolunteer import verify_volunteer_bp
from .Caretaker.CreateVetRequest import create_vet_request_bp
from .Caretaker.GetAllUnverifiedVolunteers import get_all_unverified_volunteers_bp
from .Caretaker.UnverifyVolunteer import unverify_volunteer_bp
from .Caretaker.ChangeReservationStatus import change_reservation_status_bp
from .Caretaker import get_all_reservations_bp
from .Caretaker import get_all_veterinarians_bp
from .Caretaker import get_all_animals_bp
from .Caretaker.UpdateWalkingSchedule import update_walking_schedule_bp
# veterinarian
from .Veterinarian import get_all_requests_by_vet_id_bp
from .Veterinarian import schedule_request_bp
from .Veterinarian import create_medical_record_bp
# volunteer
from .Volunteer import create_reservation_bp
from .Volunteer import get_reservations_by_volunteer_id_bp
from .Volunteer import delete_reservation_bp
# authorization
from .Authorization.SignIn import sign_in_bp
from .Authorization.SignUp import sign_up_bp
# public
from .Public import get_animal_info_by_id_bp
from .Public import filter_animals_bp
__all__ = [
    'get_all_reservations_bp',
    'change_reservation_status_bp',
    'unverify_volunteer_bp','get_all_users_bp',
    'get_all_unverified_volunteers_bp',
    'create_caretaker_bp',
    'create_veterinarian_bp',
    'create_walking_schedule_bp',
    'create_animal_bp',
    'sign_in_bp',
    'sign_up_bp',
    'verify_volunteer_bp',
    'create_vet_request_bp',
    'get_all_veterinarians_bp',
    'get_all_animals_bp',
    'update_user_bp',
    'create_reservation_bp',
    'get_animal_info_by_id_bp',
    'filter_animals_bp',
    'get_all_requests_by_vet_id_bp',
    'schedule_request_bp',
    'create_medical_record_bp',
    'get_reservations_by_volunteer_id_bp',
    'delete_reservation_bp',
    'update_walking_schedule_bp'
    ]
