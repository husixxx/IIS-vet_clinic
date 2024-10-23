from flask import jsonify, Blueprint, request
from flask_login import login_required, current_user

check_session_bp = Blueprint('check_session', __name__)

@check_session_bp.route('/authorization/check_session', methods=['GET'])
def check_session():
    """
    Check Session
    ---
    responses:
        200:
            description: User info
        400:
            description: Expired
    """
    # Ověření, zda je uživatel přihlášený a session je platná
    if current_user.is_authenticated:
        return jsonify(
            {   'status': 'active',
                'user_id': current_user.id,
                'username': current_user.username,
                'role_id': current_user.role_id
            }), 200
    else:
        return jsonify({'status': 'expired'}), 400