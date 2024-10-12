from flask import Blueprint, request, jsonify
from src.usecases import UnregisteredUseCase

sign_up_bp = Blueprint('sign_up', __name__)

@sign_up_bp.route('/authorization/sign_up', methods=['POST'])
def sign_up():
    """Sign up
    ---
    parameters:
      - name: username
        in: query
        type: string
        required: true
      - name: email
        in: query
        type: string
        required: true
      - name: password
        in: query
        type: string
        required: true
      - name: name
        in: query
        type: string
        required: true
    responses:
      201:
        description: Sign up successful
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
        description: Invalid input
    """


    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    name = request.args.get('name')



    use_case = UnregisteredUseCase()
    user = use_case.sign_up(username,password, email, name)

    return jsonify({
        'id': user.id,
        'email': user.email,
        'role_id': user.role_id
    }), 201