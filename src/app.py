from flask import Flask, request, jsonify
from backend import db
from backend import VolunteerUseCase, AdminUseCase
from flasgger import Swagger
import os


app = Flask(__name__)

# SQLite database
DATABASE_URI = 'postgresql://husic:husic@localhost:5432/iis'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Init app
db.init_app(app)

swagger = Swagger(app)

# Create tables
with app.app_context():
    db.create_all()
    
    

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/animal', methods=['POST'])
def create_animal():
    """
    Create a new animal.
    ---
    parameters:
      - name: name
        required: true
        type: string
        in: query
      - name: species
        required: true
        type: string
        in: query
      - name: age
        required: false
        type: integer
        in: query
      - name: photo
        required: false
        type: string
        in: query
      - name: history
        required: false
        type: string
        in: query
      - name: caretaker_id
        required: false
        type: integer
        in: query
    responses:
      201:
        description: Animal created
      400:
        description: Invalid input
    """
    # Získanie parametrov z requestu
    name = request.args.get('name')
    species = request.args.get('species')
    age = request.args.get('age', type=int)
    photo = request.args.get('photo')
    history = request.args.get('history')
    caretaker_id = request.args.get('caretaker_id', type=int)

    # Vytvorenie use case a zvieraťa
    use_case = AdminUseCase()
    
    try:
        animal = use_case.create_animal(name, species, age, photo, history, caretaker_id)
        return jsonify({
            'id': animal.id,
            'name': animal.name,
            'species': animal.species,
            'age': animal.age,
            'photo': animal.photo,
            'history': animal.history,
            'status': animal.status,
            'caretaker_id': animal.caretaker_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    
    
    
@app.route('/caretaker', methods=['POST'])
def create_caretaker():
    """Create a new caretaker.
    ---
    parameters:
      - name: name
        required: true
        type: string
        in: query
      - name: email
        required: true
        type: string
        in: query
    responses:
      201:
        description: Caretaker created
      400:
        description: Invalid input
      409:
        description: User with this email already exists
    """
    # Získanie parametrov z requestu
    name = request.args.get('name')
    email = request.args.get('email')

    # Vytvorenie use case a caretakera
    use_case = AdminUseCase()

    try:
        caretaker = use_case.create_caretaker(name, email)
        return jsonify({
            'id': caretaker.id,
            'name': caretaker.name,
            'email': caretaker.email,
            'role_id': caretaker.role_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409  # Konflikt - existujúci používateľ
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Neplatný vstup









@app.route('/walking_schedule', methods=['POST'])
def create_walking_schedule():
    """Create a walking schedule
    ---
    parameters:
      - name: animal_id
        in: query
        type: integer
        required: true
      - name: volunteer_id
        in: query
        type: integer
        required: true
      - name: start_time
        in: query
        type: string
        required: true
      - name: end_time
        in: query
        type: string
        required: true
      - name: status
        in: query
        type: string
        required: true
    responses:
      200:
        description: Walking schedule created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            animal_id:
              type: integer
            volunteer_id:
              type: integer
            start_time:
              type: string
            end_time:
              type: string
            status:
              type: string
      400:
        description: Invalid input
    """
    
    
    animal_id = request.args.get('animal_id', type=int)
    volunteer_id = request.args.get('volunteer_id', type=int)
    start_time = request.args.get('start_time', type=str)
    end_time = request.args.get('end_time', type=str)
    status = request.args.get('status', type=str)


    volunteer_use_case = VolunteerUseCase()
    walking_schedule = volunteer_use_case.create_walking_schedule(animal_id, volunteer_id, start_time, end_time, status)

    return {
        'id': walking_schedule.id,
        'animal_id': walking_schedule.animal_id,
        'volunteer_id': walking_schedule.volunteer_id,
        'start_time': walking_schedule.start_time,
        'end_time': walking_schedule.end_time,
        'status': walking_schedule.status
    }, 200





if __name__ == '__main__':
    app.run(debug=True)
