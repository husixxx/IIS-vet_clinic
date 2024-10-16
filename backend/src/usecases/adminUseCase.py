from src.models import Animal, User
from src.repository import Repository
from werkzeug.security import generate_password_hash

class AdminUseCase:
    
    def __init__(self):
        self.animal_repository = Repository(Animal)
        self.user_repository = Repository(User)
    
    def create_animal(self, name: str, species: str, age: int = None, photo: str = None, history: str = None, caretaker_id: int = None) -> Animal:
        new_animal = Animal(
            name=name,
            species=species,
            age=age,
            photo=photo,
            history=history,
            status='available',  # predpokladaný predvolený status
            caretaker_id=caretaker_id
        )
        
        self.animal_repository.add(new_animal)
        return new_animal
    
    def create_caretaker(self, name: str, email: str, username: str, password: str) -> User:
        # Zkontrolování existence osoby
        existing_person = User.query.filter_by(username=username).first()

        if existing_person:
            # Pokud osoba existuje, můžete vrátit její ID nebo provést jinou akci
            raise ValueError("User with this username already exists")

        new_user = User(name=name, email=email, username=username, role_id=3, password=generate_password_hash(password), verified=True)
        
        self.user_repository.add(new_user)
        return new_user
    
    def create_veterinarian(self, name: str, email: str, username: str, password: str) -> User:
        # Zkontrolování existence osoby
        existing_person = User.query.filter_by(username=username).first()

        if existing_person:
            # Pokud osoba existuje, můžete vrátit její ID nebo provést jinou akci
            raise ValueError("User with this username already exists")

        new_user = User(name=name, email=email, username=username, role_id=2, password=generate_password_hash(password), verified=True)
        
        self.user_repository.add(new_user)
        return new_user
    
    def get_all_users(self) -> list:
        return self.user_repository.get_all()
    
    def update_user(self, user_id: int, name: str, email: str, username: str, password: str, verified: bool, role_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        user.name = name
        user.email = email
        user.username = username
        user.password = generate_password_hash(password)
        user.verified = verified
        user.role_id = role_id
        self.user_repository.update(user)
    