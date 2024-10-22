from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from src.usecases import CaretakerUseCase

get_all_reservations_bp = Blueprint('get_all_reservations', __name__)

@get_all_reservations_bp.route('/caretaker/get_all_reservations', methods=['GET'])
@login_required
def get_all_reservations():
  """Get all reservations
  ---
  responses:
    200:
      description: All reservations
    400:
      description: No reservations found. 
  """
  if current_user.role.name != 'caretaker':
    return jsonify({'error': 'Only caretakers can cancel vet requests'}), 403
  use_case = CaretakerUseCase()
  try:
    reservations = use_case.get_all_reservations()
    return jsonify([{
      'id' : reservation.id,
      'animal_id' : reservation.animal_id,
      'volunteer_username' : reservation.volunteer.username,
      'start_time' : reservation.start_time,
      'end_time' : reservation.end_time,
      'status' : reservation.status,
    } for reservation in reservations]), 200
  except Exception as e:
    return jsonify({
      'error': str(e)
    }), 400 