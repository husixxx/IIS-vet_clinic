from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

update_animal_bp = Blueprint('update_animal', __name__)
@update_animal_bp.route('/caretaker/update_animal', methods=['PUT'])
def update_animal():
  """
  Update animal.
  ---
  parameters:
    - name: animal_id
      required: true
      type: integer
      in: query
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
    200:
      description: Updated
    400:
      description: Invalid input      
  """


  animal_id = request.args.get('animal_id')
  name = request.args.get('name')
  breed = request.args.get('breed')
  age = request.args.get('age')
  history = request.args.get('history')
  description = request.args.get('description')
  sex = request.args.get('sex')

  use_case = CaretakerUseCase()
  try:
    use_case.update_animal(animal_id, name, breed, age, history, description, sex)
    return jsonify({'message': 'Animal updated'}), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 400
