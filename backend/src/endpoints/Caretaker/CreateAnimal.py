import base64
from flask import Blueprint, request, jsonify
from flask_login import *
from src.usecases import CaretakerUseCase

create_animal_bp = Blueprint("create_animal", __name__)


@create_animal_bp.route("/caretaker/animal", methods=["POST"])
@login_required
def create_animal():
    """
    Create a new animal.
    ---
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              name:
                type: string
                description: "Name of the animal"
                example: "Rex"
                required: true
              breed:
                type: string
                description: "Breed of the animal"
                example: "Jack Russell Terrier"
                required: true
              age:
                type: integer
                description: "Age"
                example: 2
                required: true
              photo:
                type: string
                format: binary
                description: "Photo"
                required: true
              history:
                type: string
                description: "History of the animal"
                example: "Found on the street"
                required: true
              description:
                type: string
                description: "Description of the animal"
                example: "Friendly and energetic"
                required: true
              sex:
                type: string
                description: "Sex"
                example: "Male"
                required: true
    responses:
      201:
        description: Animal created
      400:
        description: Invalid input
    """

    if current_user.role.name != "caretaker":
        return jsonify({"error": "Only caretakers can create animals"}), 403

    # Získanie parametrov z requestu
    name = request.form.get("name")
    breed = request.form.get("breed")
    age = request.form.get("age", type=int)
    photo = request.files.get("photo")  # File upload
    history = request.form.get("history")
    description = request.form.get("description")
    sex = request.form.get("sex")

    # Vytvorenie use case a zvieraťa
    use_case = CaretakerUseCase()

    if photo:
        photo_data = photo.read()
    else:
        photo_data = None

    try:
        animal = use_case.create_animal(
            name, breed, age, photo_data, history, description, sex
        )
        if animal.photo:
            photo_base64 = base64.b64encode(animal.photo).decode("utf-8")
        else:
            photo_base64 = None
        return (
            jsonify(
                {
                    "id": animal.id,
                    "name": animal.name,
                    "breed": animal.breed,
                    "age": animal.age,
                    "photo": photo_base64,
                    "history": animal.history,
                    "description": animal.description,
                    "sex": animal.sex,
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
