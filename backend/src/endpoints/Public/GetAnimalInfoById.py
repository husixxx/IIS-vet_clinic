from flask import Blueprint, request, jsonify
from src.usecases import AnimalUseCase
import logging

get_animal_info_by_id_bp = Blueprint('get_animal_info_by_id', __name__)

@get_animal_info_by_id_bp.route('/animal/info', methods=['GET'])
def get_animal_info_by_id():
    """
    Get animal information by id.
    ---
    parameters:
      - name: animal_id
        required: true
        type: integer
        in: query
    responses:
      200:
        description: Animal information retrieved
      400:
        description: Invalid input
    """
    animal_id = request.args.get('animal_id', type=int)
    use_case = AnimalUseCase()
    
    try:
      animal_info = use_case.get_animal_info_by_id(animal_id)
      logging.error(f"Animal info fetched: {animal_info}")
      return animal_info, 200
    except Exception as e:
      logging.error(f"Error fetching animal info: {e}")
      return jsonify({'error': str(e)}), 400
