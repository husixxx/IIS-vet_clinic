from flask_sqlalchemy import SQLAlchemy

# Create Instance for db
db = SQLAlchemy()

# IDK about this import
from .models import Person, Animal 