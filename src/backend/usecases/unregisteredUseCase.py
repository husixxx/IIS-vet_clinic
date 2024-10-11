from backend.models import User
from backend.repository import Repository
from werkzeug.security import generate_password_hash

class UnregisteredUseCase:
    def __init__(self):
        self.user_repository = Repository(User)

    def sign_up(self, username: str, password: str, email: str, name: str) -> User:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValueError("User with this username already exists")

        new_user = User(username=username, password=generate_password_hash(password), email=email, name=name, role_id=5)
        self.user_repository.add(new_user)
        return new_user