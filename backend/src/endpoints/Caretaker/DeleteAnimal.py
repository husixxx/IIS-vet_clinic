from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
from flask_login import login_required, current_user

delete_animal_bp = Blueprint("delete_animal", __name__)


@delete_animal_bp.route("/caretaker/delete_animal", methods=["DELETE"])
@login_required
def delete_animal():
    """
    Delete animal.
    ---
    parameters:
      - name: animal_id
        required: true
        type: int
        in: query
    responses:
        200:
            description: Deleted
        400:
            description: Invalid input
        403:
            description: Unknown operation
    """

    if current_user.role.name != "caretaker":
        return (
            jsonify({"error": f"Unknown operation for {current_user.role.name}"}),
            403,
        )

    animal_id = request.args.get("animal_id")
    use_case = CaretakerUseCase()

    try:
        use_case.delete_animal(animal_id)
        return jsonify({"message": "Animal deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
