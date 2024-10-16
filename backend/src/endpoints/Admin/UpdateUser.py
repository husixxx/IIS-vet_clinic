from flask import Blueprint, request, argsify
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
  """
  user_id = request.args.get('user_id')
  name = request.args.get('name')
  email = request.args.get('email')
  username = request.args.get('username')
  password = request.args.get('password')
  verified = request.args.get('verified')
  role_id = request.args.get('role_id')

  use_case = AdminUseCase()
  try:
    use_case.update_user(user_id, name, email, username, password, verified, role_id)
    return argsify({'message': 'User updated'}), 200
  except Exception as e:
    return argsify({'error': str(e)}), 400