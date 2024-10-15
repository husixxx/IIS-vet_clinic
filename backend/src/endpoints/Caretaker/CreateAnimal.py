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
      in: formData
    - name: breed
      required: true
      type: string
      in: formData
    - name: age
      required: true
      type: integer
      in: formData
    - name: photo
      required: true
      type: file  # Nahrávanie súboru
      in: formData
    - name: history
      required: true
      type: string
      in: formData
    - name: description
      required: true
      type: string
      in: formData
    - name: sex
      required: true
      type: string
      in: formData
  responses:
    201:
      description: Animal created
    400:
      description: Invalid input
  """
  # Získanie parametrov z requestu
  name = request.form.get('name')
  breed = request.form.get('breed')
  age = request.form.get('age', type=int)
  photo = request.files.get('photo')  # File upload
  history = request.form.get('history')
  description = request.form.get('description')
  sex = request.form.get('sex')

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
