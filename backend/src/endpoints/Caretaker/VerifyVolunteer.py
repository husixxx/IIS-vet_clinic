from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

verify_volunteer_bp = Blueprint('verify_volunteer', __name__)

@verify_volunteer_bp.route('/caretaker/verify_volunteer', methods=['POST'])
def verify_volunteer():
    """
    Verify a volunteers account.
    ---
    parameters:
      - username: username 
        required: true
        type: string
        in: query
    responses:
        200:
            description: Volunteer verified
        400:
            description: User not found/User already validated.
        
            
    """
    
    
    username = request.args.get('username')
    use_case = CaretakerUseCase()
    try:
        volunteer = use_case.verify_volunteer(username)
        return jsonify({
            'id': volunteer.id,
            'username': volunteer.username,
            'verified': volunteer.verified,
            'role_id': volunteer.role_id
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400
    