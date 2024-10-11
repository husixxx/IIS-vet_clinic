from flask import Blueprint, request, jsonify
from backend import AdminUseCase

create_caretaker_bp = Blueprint('create_caretaker', __name__)

@create_caretaker_bp.route('/admin/caretaker', methods=['POST'])
def create_caretaker():
    """Create a new caretaker.
    ---
    parameters:
      - name: name
        required: true
        type: string
        in: query
      - name: email
        required: true
        type: string
        in: query
    responses:
      201:
        description: Caretaker created
      400:
        description: Invalid input
      409:
        description: User with this email already exists
    """
    # Získanie parametrov z requestu
    name = request.args.get('name')
    email = request.args.get('email')



    # Vytvorenie use case a caretakera
    use_case = AdminUseCase()

    try:
        caretaker = use_case.create_caretaker(name, email)
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
