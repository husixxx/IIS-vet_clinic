from flask import Blueprint, request, jsonify
from src.usecases import VeterinarianUseCase

get_all_requests_by_vet_id_bp = Blueprint('get_all_requests_by_vet_id', __name__)

@get_all_requests_by_vet_id_bp.route('/veterinarian/get_all_requests_by_vet_id', methods=['GET'])
def get_all_requests_by_vet_id():
  """
  Get all requests by veterinarian ID.
  ---
  parameters:
    - name: vet_id
      in: query
      required: true
      type: integer
  responses:
    200:
      description: Successfully retrieved all requests
    400:
      description: No requests found
  """
  
  vet_id = request.args.get('vet_id')
  use_case = VeterinarianUseCase()
  try:
    requests = use_case.get_all_requests_by_vet_id(vet_id=vet_id)
    return jsonify([{
      'id' : request_vet.id,
      'animal_id' : request_vet.animal_id,
      'vet_id' : request_vet.veterinarian_id,
      'start_time' : request_vet.request_date,
      'status' : request_vet.status,
      'description' : request_vet.description,
    } for request_vet in requests]), 200
  except Exception as e:
    return jsonify({
      'error': str(e)
    }), 400