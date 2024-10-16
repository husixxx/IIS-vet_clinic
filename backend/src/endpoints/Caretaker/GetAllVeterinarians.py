from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

get_all_veterinarians_bp = Blueprint('get_all_veterinarians', __name__)

@get_all_veterinarians_bp.route('/caretaker/veterinarians', methods=['GET'])
def get_all_veterinarians():
    """Get all veterinarians.
    ---
    responses:
      200:
        description: List of all veterinarians
      400:
        description: Invalid input
    """
    use_case = CaretakerUseCase()
    
    try:
        veterinarians = use_case.get_all_veterinarians()
        return jsonify([{
            'username': veterinarian.username,
            'name': veterinarian.name,
        } for veterinarian in veterinarians]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
