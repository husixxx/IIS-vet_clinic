from flask import Blueprint, request, jsonify
from src.usecases import AdminUseCase
from flask_login import login_required, current_user

get_all_users_bp = Blueprint("get_all_users", __name__)


@get_all_users_bp.route("/admin/users", methods=["GET"])
@login_required
def get_all_users():
    """Get all users.
    ---
    responses:
      200:
        description: List of all users
      400:
        description: Invalid input
    """

    if current_user.role.name != "admin":
        return (
            jsonify({"error": f"Unknown operation for {current_user.role.name}"}),
            403,
        )

    use_case = AdminUseCase()
    try:
        users = use_case.get_all_users()
        return (
            jsonify(
                [
                    {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "verified": user.verified,
                        "role": user.role.name,
                        "username": user.username,
                    }
                    for user in users
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
