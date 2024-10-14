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
    - name: breed
      required: true
      type: string
      in: query
    - name: age
      required: true
      type: integer
      in: query
    - name: photo
      required: true
      type: string
      in: query
    - name: history
      required: true
      type: string
      in: query
    - name: description
      required: true
      type: string
      in: query
    - name: sex
      required: true
      type: string
      in: query
  responses:
    201:
      description: Animal created
    400:
      description: Invalid input
  """
  # Získanie parametrov z requestu
  name = request.args.get('name')
  breed = request.args.get('breed')
  age = request.args.get('age', type=int)
  photo = request.args.get('photo')
  history = request.args.get('history')
  description = request.args.get('description')
  sex = request.args.get('sex')

  # Vytvorenie use case a zvieraťa
  use_case = CaretakerUseCase()
  
  try:
    animal = use_case.create_animal(name, breed, age, photo, history, description, sex)
    return jsonify({
        'id': animal.id,
        'name': animal.name,
        'breed': animal.breed,
        'age': animal.age,
        'photo': animal.photo,
        'history': animal.history,
        'description': animal.description
    }), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 400
