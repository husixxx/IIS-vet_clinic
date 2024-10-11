from flask import Blueprint

from .Admin.CreateCaretaker import create_caretaker_bp

from .Caretaker.CreateWalkingSchedule import create_walking_schedule_bp
from .Caretaker.CreateAnimal import create_animal_bp

__all__ = ['create_caretaker_bp', 'create_walking_schedule_bp', 'create_animal_bp']