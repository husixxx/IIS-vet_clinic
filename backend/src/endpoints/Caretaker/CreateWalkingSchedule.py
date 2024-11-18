from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
from ..services import is_valid_timestamp
from flask_login import login_required, current_user

create_walking_schedule_bp = Blueprint("create_walking_schedule", __name__)


@create_walking_schedule_bp.route("/caretaker/walking_schedule", methods=["POST"])
@login_required
def create_walking_schedule():
    """Create a walking schedule
    ---
    parameters:
      - name: animal_id
        in: query
        type: integer
        required: true
      - name: start_time
        in: query
        type: string
        required: true
      - name: end_time
        in: query
        type: string
        required: true
    responses:
      200:
        description: Walking schedule created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            animal_id:
              type: integer
            volunteer_username:
              type: string
            start_time:
              type: string
            end_time:
              type: string
            status:
              type: string
      400:
        description: Invalid input
    """
    if current_user.role.name != "caretaker":
        return jsonify({"error": "Only caretakers can cancel vet requests"}), 403

    animal_id = request.args.get("animal_id", type=int)
    start_time = request.args.get("start_time", type=str)
    end_time = request.args.get("end_time", type=str)

    if not is_valid_timestamp(start_time) or not is_valid_timestamp(end_time):
        return (
            jsonify(
                {
                    "error": "Invalid date time",
                    "start_time": start_time,
                    "end_time": end_time,
                }
            ),
            400,
        )

    caretaker_use_case = CaretakerUseCase()
    try:

        walking_schedule = caretaker_use_case.create_walking_schedule(
            animal_id, start_time, end_time
        )
        return (
            jsonify(
                {
                    "id": walking_schedule.id,
                    "animal_id": walking_schedule.animal_id,
                    "start_time": walking_schedule.start_time,
                    "end_time": walking_schedule.end_time,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
