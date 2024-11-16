from flask import Flask, request, jsonify, session
from flask_login import LoginManager
from flasgger import Swagger
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import db

from .models import *
from .usecases import *
from .endpoints import *

from flask_cors import *


def create_app():

    app = Flask(__name__)

    app.config["SWAGGER"] = {
        "openapi": "3.0.0",  # open api version
        "info": {
            "title": "Husic API",
            "description": "API documentation with OpenAPI 3.0.3",
            "version": "1.0.0",
        },
    }

    CORS(
        app,
        resources={
            r"/*": {  # Allow all routes
                "origins": [
                    "http://127.0.0.1:5173",
                    "http://localhost:5342",
                    "http://localhost:5000",
                    "http://localhost:5173",
                ],
                "supports_credentials": True,
            }
        },
        supports_credentials=True,
    )

    # Database
    DATABASE_URI = "postgresql://husic:husic@postgres:5432/iis"
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "husic"  # session secret key

    # not sure if this is needed
    Migrate(app, db)

    db.init_app(app)
    # Swagger documentation
    Swagger(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def make_session_not_permanent():
        session.permanent = False  # Session vyprší po zavretí prehliadača

    # Create tables
    with app.app_context():
        db.create_all()
        seed_roles()
        seed_admin()

    # Admin
    app.register_blueprint(create_caretaker_bp)
    app.register_blueprint(create_veterinarian_bp)
    app.register_blueprint(get_all_users_bp)
    app.register_blueprint(update_user_bp)
    app.register_blueprint(delete_user_bp)
    # Authorization
    app.register_blueprint(sign_in_bp)
    app.register_blueprint(sign_up_bp)
    app.register_blueprint(check_session_bp)
    app.register_blueprint(sign_out_bp)

    # Caretaker
    app.register_blueprint(create_walking_schedule_bp)
    app.register_blueprint(create_animal_bp)
    app.register_blueprint(verify_volunteer_bp)
    app.register_blueprint(create_vet_request_bp)
    app.register_blueprint(unverify_volunteer_bp)
    app.register_blueprint(change_reservation_status_bp)
    app.register_blueprint(get_all_reservations_bp)
    app.register_blueprint(get_all_veterinarians_bp)
    app.register_blueprint(get_all_animals_bp)
    app.register_blueprint(filter_animals_bp)
    app.register_blueprint(get_all_vet_requests_bp)
    app.register_blueprint(cancel_vet_request_bp)

    # Veterinarian
    app.register_blueprint(get_all_requests_by_vet_id_bp)
    app.register_blueprint(schedule_request_bp)
    app.register_blueprint(create_medical_record_bp)

    # public
    app.register_blueprint(get_all_unverified_volunteers_bp)
    app.register_blueprint(get_animal_info_by_id_bp)
    app.register_blueprint(get_all_breeds_bp)

    # Volunteer
    app.register_blueprint(create_reservation_bp)
    app.register_blueprint(get_reservations_by_volunteer_id_bp)
    app.register_blueprint(delete_reservation_bp)
    return app


def seed_roles():
    # Define the roles to be created
    roles = [
        {"name": "volunteer"},
        {"name": "veterinarian"},
        {"name": "caretaker"},
        {"name": "admin"},
        {"name": "registered"},
    ]

    # avoid duplicates
    with db.session.begin():  # current session
        for role in roles:
            existing_role = Role.query.filter_by(name=role["name"]).first()
            if not existing_role:
                new_role = Role(name=role["name"])
                db.session.add(new_role)
        db.session.commit()


def seed_admin():
    existing_admin = User.query.filter_by(username="admin").first()
    if not existing_admin:
        Admin = User(
            name="admin",
            email="admin@admin.sk",
            username="admin",
            password=generate_password_hash("admin"),
            role_id=4,
            verified=True,
        )
        db.session.add(Admin)
        db.session.commit()
