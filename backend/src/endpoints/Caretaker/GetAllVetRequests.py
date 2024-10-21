from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

get_all_vet_requests_bp = Blueprint('get_all_vet_requests', __name__)

@get_all_vet_requests_bp.route('/caretaker/get_all_vet_requests', methods=['GET'])

def get_all_vet_requests():
  """Get all vet requests
  ---
  responses:
    200:
      description: All vet requests
    400:
      description: No vet requests found
  """
  
  use_case = CaretakerUseCase()
  try:
    vet_requests = use_case.get_all_vet_requests()
    return jsonify([{
      'id': vet_request.id,
      'animal_id': vet_request.animal_id,
      'request_date': vet_request.request_date,
      'status': vet_request.status,
      'description': vet_request.description,
      'veterinarian_username': vet_request.veterinarian.username
    } for vet_request in vet_requests])
  except Exception as e:
    return jsonify({
      'error': str(e)
    }), 400