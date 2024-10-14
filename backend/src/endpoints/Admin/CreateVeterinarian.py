from flask import Blueprint, request, jsonify
from src.usecases import AdminUseCase

create_veterinarian_bp = Blueprint('create_veterinarian', __name__)

@create_veterinarian_bp.route('/admin/veterinarian', methods=['POST'])
def create_veterinarian():
  """Create a new veterinarian.
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
      description: Veterinarian created
    400:
      description: Invalid input
    409:
      description: User with this email already exists
  """
  # Získanie parametrov z requestu
  name = request.args.get('name')
  email = request.args.get('email')
  username = request.args.get('username')
  password = request.args.get('password')



  # Vytvorenie use case a caretakera
  use_case = AdminUseCase()

  try:
      caretaker = use_case.create_veterinarian(name, email, username, password)
      return jsonify({
          'id': caretaker.id,
          'name': caretaker.name,
          'email': caretaker.email,
          'role_id': caretaker.role_id
      }), 201
  except ValueError as e:
      return jsonify({'error': str(e)}), 409  # Konflikt - existujúci používateľ
  except Exception as e:
      return jsonify({'error': str(e)}), 400  # Neplatný vstup