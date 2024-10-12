# backend/models/__init__.py
from .animal import Animal
from .user import User
from .medical_record import MedicalRecord
from .walking_schedule import WalkingSchedule
from .role import Role
# Pridajte ďalšie modely podľa potreby

# Možno je dobré mať aj prístup k db
from backend import db