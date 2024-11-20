from flask import Blueprint, request, jsonify
from src.usecases import AdminUseCase
from flask_login import login_required, current_user

unverify_user_bp = Blueprint("unverify_user", __name__)

@unverify_user_bp.route("/admin/unverify_user", methods=["POST"])
@login_required
def unverify_volunteer():
  """Unverify a user account
  ---
  parameters:
    - name: id
      required: true
      type: int
      in: query
  responses:
    200:
      description: User unverified
    400:
      description: User not found/User already unverified.
  """
  
  if current_user.role.name != "admin":
    return jsonify({"error": "Only admins can unverify users"}), 403

  id = request.args.get("id")
  use_case = AdminUseCase()
  try:
    user = use_case.unverify_user(id)
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