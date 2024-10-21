from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

cancel_vet_request_bp = Blueprint('cancel_vet_request', __name__)

@cancel_vet_request_bp.route('/caretaker/cancel_vet_request', methods=['DELETE'])
def cancel_vet_request():
  """
  Cancel veterinarian request.
  ---
  parameters:
    - name: vet_request_id
      required: true
      type: integer
      in: query
  responses:
    200:
      description: Vet request canceled
    400:
      description: Request not found
  """
  
  vet_request_id = request.args.get('vet_request_id')
  
  use_case = CaretakerUseCase()
  try:
    use_case.cancel_vet_request(vet_request_id)
    return jsonify ({
      'message': 'Reservation deleted'
    }), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 400