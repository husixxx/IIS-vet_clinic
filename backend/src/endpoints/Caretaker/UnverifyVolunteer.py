from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

unverify_volunteer_bp = Blueprint("unverify_volunteer", __name__)


@unverify_volunteer_bp.route("/caretaker/unverify_volunteer", methods=["POST"])
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
            description: User not found/User already unverified.
    """

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
