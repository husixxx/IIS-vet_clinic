from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

create_animal_bp = Blueprint('create_animal', __name__)

@create_animal_bp.route('/caretaker/animal', methods=['POST'])
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
    use_case = CaretakerUseCase()
    
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
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
