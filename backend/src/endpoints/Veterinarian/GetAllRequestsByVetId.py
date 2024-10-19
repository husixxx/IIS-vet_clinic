from flask import Blueprint, request, jsonify
from src.usecases import VeterinarianUseCase

get_all_requests_by_vet_id_bp = Blueprint('get_all_requests_by_vet_id', __name__)

@get_all_requests_by_vet_id_bp.route('/veterinarian/get_all_requests_by_vet_id', methods=['GET'])
def get_all_requests_by_vet_id():
  """Get all requests by vet id
  ---
  responses:
    200:
      description: All requests
    400:
      description: No requests found. 
  """
  
  use_case = VeterinarianUseCase()
  try:
    requests = use_case.get_all_requests_by_vet_id()
    return jsonify([{
      'id' : request.id,
      'animal_id' : request.animal_id,
      'vet_id' : request.vet_id,
      'start_time' : request.start_time,
      'end_time' : request.end_time,
      'status' : request.status,
      'description' : request.description,
    } for request in requests]), 200
  except Exception as e:
    return jsonify({
      'error': str(e)
    }), 400