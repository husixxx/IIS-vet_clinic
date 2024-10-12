# src/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import models (this ensures they are registered with SQLAlchemy)
from .models import *