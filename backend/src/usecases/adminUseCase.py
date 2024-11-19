from src.models import Animal, User
from src.repository import Repository, PublicRepository
from werkzeug.security import generate_password_hash

"""
Use case class handling administrator-related operations for user management.

Attributes:
    user_repository (Repository): Repository for handling User entities
    public_repository (PublicRepository): Repository for complex public operations

Methods:
    create_caretaker: Creates a new caretaker user account
    create_veterinarian: Creates a new veterinarian user account
    get_all_users: Retrieves all users in the system
    update_user: Updates existing user information
    delete_user: Deletes a user based on their role (except admin)

Note:
    Role IDs:
    1 - Volunteer
    2 - Veterinarian
    3 - Caretaker
    4 - Admin
    5 - Unverified Volunteer
"""


class AdminUseCase:

    def __init__(self):
        self.user_repository = Repository(User)
        self.public_repository = PublicRepository()

    def create_caretaker(
        self, name: str, email: str, username: str, password: str
    ) -> User:

        # Check if person exists
        existing_person = User.query.filter_by(username=username).first()
        existing_person_email = User.query.filter_by(email=email).first()

        if existing_person:
            raise ValueError("User with this username already exists")

        if existing_person_email:
            raise ValueError("User with this email already exists")

        new_user = User(
            name=name,
            email=email,
            username=username,
            role_id=3,
            password=generate_password_hash(password),
            verified=True,
        )

        self.user_repository.add(new_user)
        return new_user

    def create_veterinarian(
        self, name: str, email: str, username: str, password: str
    ) -> User:

        # Check if person exists
        existing_person = User.query.filter_by(username=username).first()

        existing_person_email = User.query.filter_by(email=email).first()

        if existing_person:
            raise ValueError("User with this username already exists")

        if existing_person_email:
            raise ValueError("User with this email already exists")

        new_user = User(
            name=name,
            email=email,
            username=username,
            role_id=2,
            password=generate_password_hash(password),
            verified=True,
        )

        self.user_repository.add(new_user)
        return new_user

    def get_all_users(self) -> list:
        return self.user_repository.get_all()

    def update_user(
        self,
        user_id: int,
        name: str,
        email: str,
        username: str,
        password: str,
        verified: bool,
        role_id: int,
    ):

        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")
        if username == "":
            raise ValueError("Username cannot be empty")
        if email == "":
            raise ValueError("Email cannot be empty")
        if name == "":
            raise ValueError("Name cannot be empty")
        
        
        user.name = name
        user.email = email
        user.username = username

        if password != "":
            user.password = generate_password_hash(password)

        user.verified = verified
        user.role_id = role_id

        self.user_repository.update(user)

    def delete_user(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        if user.role_id == 1:
            self.public_repository.delete_volunteer(user_id)

        if user.role_id == 2:
            self.public_repository.delete_veterinarian(user_id)

        if user.role_id == 3:
            self.public_repository.delete_user(user_id)

        if user.role_id == 4:
            raise ValueError("Cannot delete admin")

        if user.role_id == 5:
            self.public_repository.delete_user(user_id)
