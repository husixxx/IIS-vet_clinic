from flask import Blueprint, jsonify
from src.usecases import CaretakerUseCase

get_all_animals_bp = Blueprint('get_all_animals', __name__)

@get_all_animals_bp.route('/caretaker/animals', methods=['GET'])
def get_all_animals():
    """Get all animals.
    ---
    responses:
      200:
        description: List of all animals
      400:
        description: Invalid input
    """
    use_case = CaretakerUseCase()
    
    try:
        animals = use_case.get_all_animals()
        return jsonify([{
            'name': animal.name,
            'breed': animal.breed,
            'age': animal.age,
            'photo': animal.photo,
            'description': animal.description,
        } for animal in animals]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
