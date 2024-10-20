from flask import Blueprint, request, jsonify
from src.usecases import AnimalUseCase

get_all_breeds_bp = Blueprint('get_all_breeds', __name__)

@get_all_breeds_bp.route('/animal/breeds', methods=['GET'])
def get_all_breeds():
    """
    Get all animal breeds.
    ---
    responses:
      200:
        description: Successfully retrieved all breeds
      400:
        description: No breeds found
    """
    use_case = AnimalUseCase()
    
    try:
      breeds = use_case.get_all_breeds()
      return jsonify(breeds), 200
    except Exception as e:
      return jsonify({'error': str(e)}), 400