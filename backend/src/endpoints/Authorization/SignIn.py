from flask import Blueprint, request, jsonify
from werkzeug.security import *
from flask_login import login_user
from src.models import User

sign_in_bp = Blueprint('sign_in', __name__)

@sign_in_bp.route('/authorization/sign_in', methods=['POST'])
def sign_in():
    """Sign in
    ---
    parameters:
      - name: username
        in: query
        type: string
        required: true
      - name: password
        in: query
        type: string
        required: true
    responses:
      200:
        description: Sign in successful
        schema:
          type: object
          properties:
            id:
              type: integer
            email:
              type: string
            role_id:
              type: integer
      400:
        description: Not found
      401:
        description: Unauthorized
    """
    username = request.args.get('username')
    password = request.args.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None:
      return jsonify({'error': 'Not found222'}), 400
    if not check_password_hash(user.password, password):
      return jsonify({'error': 'Password bad'}), 400
      
    
    if not user.verified:
        return jsonify({'error': 'Unauthorized'}), 401
    
    login_user(user)
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'role_id': user.role_id
    }), 200