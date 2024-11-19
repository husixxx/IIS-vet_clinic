from flask import Blueprint, request, jsonify
from src.usecases import VeterinarianUseCase
from ..services import is_valid_date
from flask_login import login_required, current_user

update_medical_record_bp = Blueprint('update_medical_record', __name__)
@update_medical_record_bp.route('/caretaker/update_medical_record', methods=['PUT'])
@login_required
def update_medical_record():
  """
  Update medical record.
  ---
  parameters:
    - name: medical_record_id
      required: true
      type: integer
      in: query
    - name: veterinarian_id
      required: true
      type: integer
      in: query
    - name: examination_date
      required: true
      type: string
      in: query
    - name: examination_type
      required: true
      type: string
      in: query
    - name: description
      required: true
      type: string
      in: query
  responses:
    200:
      description: Updated
    400:
      description: Invalid input
    403:
      description: Unknown operation
  """

  if current_user.role.name != "veterinarian":
        return (
            jsonify({"error": f"Unknown operation for {current_user.role.name}"}),
            403,
        )

  medical_record_id = request.args.get('medical_record_id')
  veterinarian_id = request.args.get('veterinarian_id')
  examination_date = request.args.get('examination_date')
  examination_type = request.args.get('examination_type')
  description = request.args.get('description')

  if not is_valid_date(examination_date):
    return jsonify({
      'error': 'Invalid date',
      'examination_date': examination_date,
    }), 400

  use_case = VeterinarianUseCase()
  try:
    use_case.update_medical_record(medical_record_id, veterinarian_id, examination_date, examination_type, description)
    return jsonify({'message': 'Medical record updated'}), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 400
