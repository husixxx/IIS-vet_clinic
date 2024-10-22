from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
from flask_login import current_user, login_required
get_all_unverified_volunteers_bp = Blueprint('get_all_unverified_volunteers', __name__)

@get_all_unverified_volunteers_bp.route('/caretaker/unverified_volunteers', methods=['GET'])
@login_required
def get_all_unverified_volunteers():
    """Get all unverified volunteers.
    ---
    responses:
      200:
        description: List of all unverified volunteers
      400:
        description: Invalid input
    """
    if current_user.role.name != 'caretaker':
      return jsonify({'error': 'Only caretakers can cancel vet requests'}), 403
    
    use_case = CaretakerUseCase()
    
    try:
        volunteers = use_case.get_all_unverified_volunteers()
        return jsonify([{
            'id': volunteer.id,
            'name': volunteer.name,
            'email': volunteer.email,
            'role_id': volunteer.role_id
        } for volunteer in volunteers]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400