from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

get_all_unverified_volunteers_bp = Blueprint('get_all_unverified_volunteers', __name__)

@get_all_unverified_volunteers_bp.route('/caretaker/unverified_volunteers', methods=['GET'])
def get_all_unverified_volunteers():
    """Get all unverified volunteers.
    ---
    responses:
      200:
        description: List of all unverified volunteers
      400:
        description: Invalid input
    """
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