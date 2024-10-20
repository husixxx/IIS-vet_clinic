from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
import logging

logging.basicConfig(level=logging.DEBUG)  # nebo INFO, pokud chceš méně detailů
logger = logging.getLogger(__name__)

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
  responses:
    200:
      description: Successfully filtered animals
    400:
      description: No animals found
  """
  
  name = request.args.get('name', type=str)
  breed = request.args.get('breed', type=str)
  age = request.args.get('age', type=int)
  availability = request.args.get('availability', type=bool)
  
  useCase = CaretakerUseCase()
  
  try:
    animals = useCase.filter_animals(name, age, breed, availability)
    logger.debug(f"Filtered animals: {[{'id': animal.id, 'name': animal.name} for animal in animals]}")
    
    return jsonify([{
      'id' : animal.id,
      'name' : animal.name,
      'age' : animal.age,
      'breed' : animal.breed,
      'description' : animal.description
      } for animal in animals]), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 400
    
    
    
