from flask import Blueprint

from .Admin.CreateCaretaker import create_caretaker_bp

from .Caretaker.CreateWalkingSchedule import create_walking_schedule_bp
from .Caretaker.CreateAnimal import create_animal_bp
from .Authorization.SignIn import sign_in_bp
from .Authorization.SignUp import sign_up_bp
from .Caretaker.VerifyVolunteer import verify_volunteer_bp
__all__ = ['create_caretaker_bp', 'create_walking_schedule_bp', 'create_animal_bp', 'sign_in_bp', 'sign_up_bp', 'verify_volunteer_bp']