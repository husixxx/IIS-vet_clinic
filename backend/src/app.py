from flask import Flask, request, jsonify
from flask_login import LoginManager
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from . import db

from .models import *
from .usecases import *
from .endpoints import *

from flask_cors import *

def create_app():
  app = Flask(__name__)
  app.config['SWAGGER'] = {
    "openapi": "3.0.0",  # Nastav verziu OpenAPI
    "info": {
        "title": "Husic API",
        "description": "API documentation with OpenAPI 3.0.3",
        "version": "1.0.0"
    }
  }

  CORS(app, resources={
    r"/*": {  # Allow all routes
        "origins": ["http://127.0.0.1:5173", "http://localhost:5342", "http://localhost:5000"],
        "supports_credentials": True
      }
  })

  # Database
  DATABASE_URI = 'postgresql://husic:husic@postgres:5432/iis'
  app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.secret_key = 'husic'  # Tajný klíč pro session

  db.init_app(app)
  swagger = Swagger(app)

  login_manager = LoginManager()
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  # login_manager.login_view = 'sign in'



  # Create tables
  with app.app_context():
    db.create_all()
    seed_roles()

  # Register blueprints(endpoints)
  app.register_blueprint(create_caretaker_bp)
  app.register_blueprint(create_walking_schedule_bp)
  app.register_blueprint(create_animal_bp)
  app.register_blueprint(sign_in_bp)
  app.register_blueprint(sign_up_bp)

  return app
      

def seed_roles():
  # Define the roles to be created
  roles = [
    {'name': 'volunteer'},
    {'name': 'veterinarian'},
    {'name': 'caretaker'},
    {'name': 'admin'},
    {'name': 'registered'}
  ]
  
  # Check if roles already exist to avoid duplication
  with db.session.begin():  # Using a context manager for the session
    for role in roles:
      existing_role = Role.query.filter_by(name=role['name']).first()
      if not existing_role:
        new_role = Role(name=role['name'])
        db.session.add(new_role)
    db.session.commit()  # Save the changes


