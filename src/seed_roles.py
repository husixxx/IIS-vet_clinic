from app import db
from backend import Role  # Import your Role model

def seed_roles():
    # Define the roles to be created
    roles = [
        {'name': 'volunteer'},
        {'name': 'veterinarian'},
        {'name': 'caretaker'}
    ]
    
    # Check if roles already exist to avoid duplication
    for role in roles:
        existing_role = Role.query.filter_by(name=role['name']).first()
        if not existing_role:
            new_role = Role(name=role['name'])
            db.session.add(new_role)
    
    db.session.commit()  # Save the changes

if __name__ == "__main__":
    from app import app
    with app.app_context():
        seed_roles()  # Call the seed function
