from backend import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Ujisti se, že ukládáš hashed hesla
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # ForeignKey to Role
    role = db.relationship('Role', back_populates='users')
    verified = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return f'<User {self.name}>'