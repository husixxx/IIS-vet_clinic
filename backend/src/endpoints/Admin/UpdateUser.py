from flask import Blueprint, request, jsonify
from src.usecases import AdminUseCase

update_user_bp = Blueprint('update_user', __name__)
@update_user_bp.route('/admin/update_user', methods=['PUT'])
def update_user():
  """
  Update user.
  ---
  parameters:
    - name: user_id
      required: true
      type: integer
      in: query
    - name: name
      required: true
      type: string
      in: query
    - name: email
      required: true
      type: string
      in: query
    - name: username
      required: true
      type: string
      in: query
    - name: password
      required: true
      type: string
      in: query
    - name: verified
      required: true
      type: boolean
      in: query
    - name: role_id
      required: true
      type: integer
      in: query
  responses:
    200:
      description: Updated
    400:
      description: Invalid input      
  """
  user_id = request.args.get('user_id')
  name = request.args.get('name')
  email = request.args.get('email')
  username = request.args.get('username')
  password = request.args.get('password')
  if password is None:
    password = ""
  verified_str = request.args.get('verified').lower()
  verified = verified_str == 'true'
  
  role_id = request.args.get('role_id')
  
  use_case = AdminUseCase()
  try:
    use_case.update_user(user_id, name, email, username, password, verified, role_id)
    return jsonify({'message': 'User updated'}), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 400