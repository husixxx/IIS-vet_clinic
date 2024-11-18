from flask import Blueprint, request, jsonify
from src.usecases import AdminUseCase
from flask_login import login_required, current_user

create_caretaker_bp = Blueprint("create_caretaker", __name__)


@create_caretaker_bp.route("/admin/caretaker", methods=["POST"])
@login_required
def create_caretaker():
    """Create a new caretaker.
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
        description: Caretaker created
      400:
        description: Invalid input
      409:
        description: User with this credentials already exists
    """
    if current_user.role.name != "admin":
        return (
            jsonify({"error": f"Unknown operation for {current_user.role.name}"}),
            403,
        )

    name = request.args.get("name")
    email = request.args.get("email")
    username = request.args.get("username")
    password = request.args.get("password")

    use_case = AdminUseCase()

    try:
        caretaker = use_case.create_caretaker(name, email, username, password)
        return (
            jsonify(
                {
                    "id": caretaker.id,
                    "name": caretaker.name,
                    "email": caretaker.email,
                    "role_id": caretaker.role_id,
                }
            ),
            201,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 409  # user exists
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # bad request
