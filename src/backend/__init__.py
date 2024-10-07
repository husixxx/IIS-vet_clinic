from flask_sqlalchemy import SQLAlchemy

# Inicializácia SQLAlchemy
db = SQLAlchemy()

# Importovanie modelov
from backend.models import *
# Importovanie use cases
from backend.usecases import *
