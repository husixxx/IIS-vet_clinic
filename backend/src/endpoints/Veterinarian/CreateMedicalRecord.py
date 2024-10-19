from flask import Blueprint, request, jsonify
from src.usecases import VeterinarianUseCase
from ..services import is_valid_date

create_medical_record_bp = Blueprint('create_medical_record', __name__)
@create_medical_record_bp.route('/veterinarian/create_medical_record', methods=['POST'])

def create_medical_record():
    """
    Create medical record
    ---
    parameters:
        - name: animal_id
          in: query
          type: int
          required: true
        - name: veterinarian_id
          in: query
          type: int
          required: true
        - name: description
            in: query
            type: str
            required: true
        - name: examination_date
            in: query
            type: str
            required: true
        - name: examination_type
            in: query
            type: str
            required: true
    ---
    responses:
        200:
            description: Medical record created
        400:
            description: Medical record not created
    """
    
    animal_id = request.args.get('animal_id')
    veterinarian_id = request.args.get('veterinarian_id')
    description = request.args.get('description')
    examination_date = request.args.get('examination_date')
    examination_type = request.args.get('examination_type')
    if not is_valid_date(examination_date):
        return jsonify({
            'error': 'Invalid date'
        }), 400
        
    use_case = VeterinarianUseCase()
    try:
        record = use_case.create_medical_record(animal_id, examination_date=examination_date, veterinarian_id=veterinarian_id, examination_type=examination_type, description=description)
        return jsonify({
            'id': record.id,
            'animal_id': record.animal_id,
            'examination_date': record.examination_date,
            'veterinarian_id': record.veterinarian_id,
            'examination_type': record.examination_type,
            'description': record.description
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400
    