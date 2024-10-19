from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

filter_animals_bp = Blueprint('filter_animals', __name__)
@filter_animals_bp.route('/filter_animals', methods=['GET'])
def filter_animals():
  """Filter animals
  ---
  parameters:
    - name: name
      in: query
      type: string
      required: false
    - name: breed
      in: query
      type: string
      required: false
    - name: age
      in: query
      type: integer
      required: false
    - name: date
      type: string
      required: false
  """
  
  name = request.args.get('name', type=str)
  breed = request.args.get('breed', type=str)
  age = request.args.get('age', type=int)
  date = request.args.get('date', type=str)
  
  
  useCase = CaretakerUseCase()
  try:
    animals = useCase.filter_animals(name, age, breed, date)
    return jsonify(animals), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 400
    
    
    
