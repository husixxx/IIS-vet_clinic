# from flask import Blueprint, request, jsonify
# from src.usecases import CaretakerUseCase
# from flask_login import login_required, current_user

# update_animal_bp = Blueprint('update_animal', __name__)
# @update_animal_bp.route('/caretaker/update_animal', methods=['PUT'])
# @login_required
# def update_animal():
#   """
#   Update animal.
#   ---
#   parameters:
#     - name: animal_id
#       required: true
#       type: integer
#       in: query
#     - name: name
#       required: true
#       type: string
#       in: query
#     - name: breed
#       required: true
#       type: string
#       in: query
#     - name: age
#       required: true
#       type: integer
#       in: query
#     - name: history
#       required: true
#       type: string
#       in: query
#     - name: description
#       required: true
#       type: string
#       in: query
#     - name: sex
#       required: true
#       type: string
#       in: query
#   responses:
#     200:
#       description: Updated
#     400:
#       description: Invalid input
#     403:
#       description: Unknown operation            
#   """

#   if current_user.role.name != "caretaker":
#         return (
#             jsonify({"error": f"Unknown operation for {current_user.role.name}"}),
#             403,
#         )

#   animal_id = request.args.get('animal_id')
#   name = request.args.get('name')
#   breed = request.args.get('breed')
#   age = request.args.get('age')
#   history = request.args.get('history')
#   description = request.args.get('description')
#   sex = request.args.get('sex')

#   use_case = CaretakerUseCase()
#   try:
#     use_case.update_animal(animal_id, name, breed, age, history, description, sex)
#     return jsonify({'message': 'Animal updated'}), 200
#   except Exception as e:
#     return jsonify({'error': str(e)}), 400

from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
from flask_login import login_required, current_user

update_animal_bp = Blueprint('update_animal', __name__)
@update_animal_bp.route('/caretaker/update_animal', methods=['PUT'])
@login_required
def update_animal():
  """
    Update an animal.
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
      200:
        description: Animal updated
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

  animal_id = request.form.get('animal_id')
  name = request.form.get("name")
  breed = request.form.get("breed")
  age = request.form.get("age", type=int)
  photo = request.files.get("photo")  # File upload
  history = request.form.get("history")
  description = request.form.get("description")
  sex = request.form.get("sex")

  if photo:
    photo_data = photo.read()
  else:
    photo_data = None
  
  use_case = CaretakerUseCase()
  try:
    use_case.update_animal(animal_id, name, breed, age, history, description, sex, photo_data)
    return jsonify({'message': 'Animal updated'}), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 400
