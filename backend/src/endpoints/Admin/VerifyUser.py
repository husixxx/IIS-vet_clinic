from flask import Blueprint, request, jsonify
from src.usecases import AdminUseCase
from flask_login import login_required, current_user

verify_user_bp = Blueprint("verify_user", __name__)


@verify_user_bp.route("/admin/verify_user", methods=["POST"])
@login_required
def verify_user():
    """Verify a user account
    ---
    parameters:
      - name: id
        required: true
        type: int
        in: query
    responses:
      200:
        description: User verified
      400:
        description: User not found/User already validated.
    """

    if current_user.role.name != "admin":
        return jsonify({"error": "Only admins can verify users"}), 403

    id = request.args.get("id")
    use_case = AdminUseCase()
    try:
        user = use_case.verify_user(id)
        return jsonify(
            {
                "id": user.id,
                "username": user.username,
                "verified": user.verified,
                "role_id": user.role_id,
            }
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
