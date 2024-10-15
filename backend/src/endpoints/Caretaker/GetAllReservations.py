from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

get_all_reservations_bp = Blueprint('get_all_reservations', __name__)

@get_all_reservations_bp.route('/caretaker/get_all_reservations', methods=['GET'])
def get_all_reservations():
  """Get all reservations
  ---
  responses:
    200:
      description: All reservations
    400:
      description: No reservations found. 
  """
  
  use_case = CaretakerUseCase()
  try:
    reservations = use_case.get_all_reservations()
    return jsonify({
      'reservations': reservations
    })
  except Exception as e:
    return jsonify({
      'error': str(e)
    }), 400