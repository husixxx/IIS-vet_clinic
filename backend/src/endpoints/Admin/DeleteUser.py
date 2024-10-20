from flask import Blueprint, request, jsonify
from src.usecases import AdminUseCase

delete_user_bp = Blueprint('delete_user', __name__)
@delete_user_bp.route('/admin/delete_user', methods=['DELETE'])

def delete_user():
    """
    Delete user.
    ---
    parameters:
      - name: user_id
        required: true
        type: int
        in: query
    responses:
        200:
            description: Deleted
        400:
            description: Invalid input      
    """
    user_id = request.args.get('user_id')
    use_case = AdminUseCase()
    
    try:
        use_case.delete_user(user_id)
        return jsonify({'message': 'User deleted'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400