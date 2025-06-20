from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from src.usecases import CaretakerUseCase
import base64

get_all_animals_bp = Blueprint("get_all_animals", __name__)


@get_all_animals_bp.route("/caretaker/animals", methods=["GET"])
@login_required
def get_all_animals():
    """Get all animals.
    ---
    responses:
      200:
        description: List of all animals
      400:
        description: Invalid input
    """
    if current_user.role.name != "caretaker":
        return jsonify({"error": "Only caretakers can cancel vet requests"}), 403

    use_case = CaretakerUseCase()

    try:
        animals = use_case.get_all_animals()
        return (
            jsonify(
                [
                    {
                        "name": animal.name,
                        "breed": animal.breed,
                        "age": animal.age,
                        "photo": (
                            base64.b64encode(animal.photo).decode("utf-8")
                            if animal.photo
                            else None
                        ),
                        "description": animal.description,
                    }
                    for animal in animals
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
