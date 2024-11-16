from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from src.usecases import CaretakerUseCase
from ..services import *
from datetime import datetime

create_vet_request_bp = Blueprint("create_vet_request", __name__)


@create_vet_request_bp.route("/caretaker/vet_request", methods=["POST"])
@login_required
def create_vet_request():
    """
    Create a new vet request.
    ---
    parameters:
      - name: animal_id
        required: true
        type: integer
        in: query
      - name: veterinarian_username
        required: true
        type: string
        in: query
      - name: request_date
        required: true
        type: string
        in: query
      - name: description
        required: true
        type: string
        in: query
    responses:
      200:
        description: Vet request created
      400:
        description: Invalid input
    """
    if current_user.role.name != "caretaker":
        return jsonify({"error": "Only caretakers can cancel vet requests"}), 403
    # Získanie parametrov z requestu
    animal_id = request.args.get("animal_id", type=int)
    veterinarian_username = request.args.get("veterinarian_username")
    request_date = request.args.get("request_date")
    description = request.args.get("description")

    # Vytvorenie use case a žiadosti
    use_case = CaretakerUseCase()

    try:
        if not is_valid_timestamp(request_date):
            raise Exception("Invalid date format.")

        vet_request = use_case.create_vet_request(
            animal_id, veterinarian_username, request_date, description
        )
        return (
            jsonify(
                {
                    "animal_id": vet_request.animal_id,
                    "veterinarian_id": vet_request.veterinarian_id,
                    "request_date": vet_request.request_date,
                    "status": vet_request.status,
                    "description": vet_request.description,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
