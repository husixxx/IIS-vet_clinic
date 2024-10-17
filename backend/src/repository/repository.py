from typing import TypeVar, Generic, List, Type, Optional
from src import db

# Define a TypeVar to represent any SQLAlchemy model type
T = TypeVar('T')

class Repository(Generic[T]):
    
    _instances = {}

    def __new__(cls, model: Type[T]):
        if model not in cls._instances:
            cls._instances[model] = super(Repository, cls).__new__(cls)
            # Iniciuj potrebné komponenty
        return cls._instances[model]
    
    def __init__(self, model: Type[T]):
        self.model = model

    def get_all(self) -> List[T]:
        """Get all records of the given model."""
        return self.model.query.all()

    def get_by_id(self, id: int) -> Optional[T]:
        """Get a single record by ID."""
        return self.model.query.get(id)
    
    def get_by_username(self, username: str) -> Optional[T]:
        """Get a single record of user by username."""
        return self.model.query.filter_by(username=username).first()

    def get_unverified_volunteers(self) -> List[T]:
        """Get all unverified volunteers."""
        return self.model.query.filter_by(verified=False).all()
    
    def add(self, entity: T) -> None:
        """Add a new entity."""
        db.session.add(entity)
        db.session.commit()

    def update(self, entity: T) -> None:
        """Update an existing entity."""
        db.session.commit()

    def delete(self, entity: T) -> None:
        """Delete an entity."""
        db.session.delete(entity)
        db.session.commit()