from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
from flask_login import login_required, current_user

unverify_volunteer_bp = Blueprint("unverify_volunteer", __name__)


@unverify_volunteer_bp.route("/caretaker/unverify_volunteer", methods=["POST"])
@login_required
def unverify_volunteer():
    """Unverify a volunteers account
    ---
    parameters:
      - name: id
        required: true
        type: int
        in: query
    responses:
        200:
            description: Volunteer unverified
        400:
            description: User not found/User already unverified.
    """
    if current_user.role.name != "caretaker":
        return jsonify({"error": "Only caretakers can verify volunteers"}), 403

    id = request.args.get("id")
    use_case = CaretakerUseCase()
    try:
        volunteer = use_case.unverify_volunteer(id)
        return jsonify(
            {
                "id": volunteer.id,
                "username": volunteer.username,
                "verified": volunteer.verified,
                "role_id": volunteer.role_id,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
