from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from src.usecases import VeterinarianUseCase
from flask_login import login_required, current_user

get_all_requests_by_vet_id_bp = Blueprint("get_all_requests_by_vet_id", __name__)


@get_all_requests_by_vet_id_bp.route(
    "/veterinarian/get_all_requests_by_vet_id", methods=["GET"]
)
@login_required
def get_all_requests_by_vet_id():
    """
    Get all requests by veterinarian ID.
    ---
    parameters:
      - name: vet_id
        in: query
        required: true
        type: integer

    responses:
      200:
        description: Successfully retrieved all requests
      400:
        description: No requests found
      403:
        description: Unknown operation
    """
    if current_user.role.name != "veterinarian":
        return jsonify({"error": "Only veterinarians can create medical records"}), 403

    if current_user.role.name != "veterinarian":
        return (
            jsonify({"error": f"Unknown operation for {current_user.role.name}"}),
            403,
        )

    vet_id = request.args.get("vet_id")
    use_case = VeterinarianUseCase()
    try:
        requests = use_case.get_all_requests_by_vet_id(vet_id=vet_id)
        return (
            jsonify(
                [
                    {
                        "id": request_vet.id,
                        "animal_id": request_vet.animal_id,
                        "animal_name": request_vet.animal.name,
                        "vet_id": request_vet.veterinarian_id,
                        "start_time": request_vet.request_date,
                        "status": request_vet.status,
                        "description": request_vet.description,
                    }
                    for request_vet in requests
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
