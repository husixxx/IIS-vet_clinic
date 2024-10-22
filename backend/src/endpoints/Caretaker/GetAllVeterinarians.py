from flask import Blueprint, jsonify
from src.usecases import CaretakerUseCase
from flask_login import login_required, current_user
get_all_veterinarians_bp = Blueprint('get_all_veterinarians', __name__)

@get_all_veterinarians_bp.route('/caretaker/veterinarians', methods=['GET'])
@login_required
def get_all_veterinarians():
    """Get all veterinarians.
    ---
    responses:
      200:
        description: List of all veterinarians
      400:
        description: Invalid input
    """
    if current_user.role.name != 'caretaker':
      return jsonify({'error': 'Only caretakers can cancel vet requests'}), 403
    use_case = CaretakerUseCase()
    
    try:
        veterinarians = use_case.get_all_veterinarians()
        return jsonify([{
            'username': veterinarian.username,
            'name': veterinarian.name,
        } for veterinarian in veterinarians]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
