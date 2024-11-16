from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
from flask_login import login_required, current_user

verify_volunteer_bp = Blueprint("verify_volunteer", __name__)


@verify_volunteer_bp.route("/caretaker/verify_volunteer", methods=["POST"])
@login_required
def verify_volunteer():
    """Verify a volunteers account
    ---
    parameters:
      - name: id
        required: true
        type: int
        in: query
    responses:
        200:
            description: Volunteer verified
        400:
            description: User not found/User already validated.
    """
    if current_user.role.name != "caretaker":
        return jsonify({"error": "Only caretakers can cancel vet requests"}), 403

    id = request.args.get("id")
    use_case = CaretakerUseCase()
    try:
        volunteer = use_case.verify_volunteer(id)
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
