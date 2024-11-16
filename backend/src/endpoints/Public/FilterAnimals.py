from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
import logging
import base64

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

filter_animals_bp = Blueprint("filter_animals", __name__)


@filter_animals_bp.route("/filter_animals", methods=["GET"])
def filter_animals():
    """Filter animals
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: false
      - name: breed
        in: query
        type: string
        required: false
      - name: age
        in: query
        type: integer
        required: false
      - name: availability
        type: string
        in: query
        required: false
    responses:
      200:
        description: Successfully filtered animals
      400:
        description: No animals found
    """

    name = request.args.get("name", type=str)
    breed = request.args.get("breed", type=str)
    age = request.args.get("age", type=int)
    availability = request.args.get("availability")
    useCase = CaretakerUseCase()

    if availability == "true" or availability == "True":
        availability = True
    elif availability == "false" or availability == "False":
        availability = False
    else:
        availability = None

    try:
        animals = useCase.filter_animals(name, age, breed, availability)
        logger.debug(
            f"Filtered animals: {[{'id': animal.id, 'name': animal.name} for animal in animals]}"
        )

        return (
            jsonify(
                [
                    {
                        "id": animal.id,
                        "name": animal.name,
                        "age": animal.age,
                        "breed": animal.breed,
                        "description": animal.description,
                        "photo": (
                            base64.b64encode(animal.photo).decode("utf-8")
                            if animal.photo
                            else None
                        ),
                    }
                    for animal in animals
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
