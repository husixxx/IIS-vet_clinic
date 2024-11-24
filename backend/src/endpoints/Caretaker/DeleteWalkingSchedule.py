from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
from flask_login import login_required, current_user

delete_walking_schedule_bp = Blueprint("delete_walking_schedule", __name__)


@delete_walking_schedule_bp.route("/caretaker/delete_walking_schedule", methods=["DELETE"])
@login_required
def delete_walking_schedule():
    """
    Delete walking schedule.
    ---
    parameters:
      - name: walking_schedule_id
        required: true
        type: int
        in: query
    responses:
        200:
            description: Deleted
        400:
            description: Invalid input
    """

    if current_user.role.name != "caretaker":
        return (
            jsonify({"error": f"Unknown operation for {current_user.role.name}"}),
            403,
        )

    walking_schedule = request.args.get("walking_schedule_id")
    use_case = CaretakerUseCase()

    try:
        use_case.delete_walking_schedule(walking_schedule)
        return jsonify({"message": "Walking schedule deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
