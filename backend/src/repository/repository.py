from typing import TypeVar, Generic, List, Type, Optional
from src import db


"""
Generic repository class implementing the repository pattern for database operations.

This class provides a generic implementation for basic CRUD operations and common queries
using SQLAlchemy. It uses the singleton pattern to ensure only one repository instance
exists per model type.

Attributes:
    _instances (dict): Class-level dictionary storing singleton instances
    model (Type[T]): SQLAlchemy model class this repository handles

Methods:
    get_all: Retrieves all records of the model type
    get_by_id: Retrieves a single record by its ID
    get_by_username: Retrieves a user record by username
    get_unverified_volunteers: Retrieves all unverified volunteer users
    add: Adds a new entity to the database
    update: Updates an existing entity in the database
    delete: Removes an entity from the database

Type Parameters:
    T: Generic type representing a SQLAlchemy model class

"""


T = TypeVar("T")


class Repository(Generic[T]):

    _instances = {}

    def __new__(cls, model: Type[T]):
        if model not in cls._instances:
            cls._instances[model] = super(Repository, cls).__new__(cls)
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
