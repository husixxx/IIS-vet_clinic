from flask import Blueprint, request, jsonify
from flask_login import *
from src.usecases import VolunteerUseCase

get_reservations_by_volunteer_id_bp = Blueprint('get_reservations_by_volunteer_id', __name__)

@get_reservations_by_volunteer_id_bp.route('/volunteer/get_reservations_by_volunteer_id', methods=['GET'])
@login_required
def get_reservations_by_volunteer_id():
  """Get all reservations by volunteer id
  ---
  parameters:
    - name: volunteer_id
      type: int
      required: true
      in: query
  responses:
    200:
      description: All reservations
    400:
      description: No reservations found. 
  """
  if current_user.role.name != "Volunteer":
    return jsonify({"error": "Only volunteers can get their reservations"}), 403
  
  volunteer_id = request.args.get('volunteer_id')
  
  use_case = VolunteerUseCase()
  try:
    reservations = use_case.get_history(volunteer_id)
    return jsonify([{
      'id' : reservation.id,
      'animal_name' : reservation.animal.name,
      'volunteer_username' : reservation.volunteer.username,
      'start_time' : reservation.start_time,
      'end_time' : reservation.end_time,
      'status' : reservation.status,
    } for reservation in reservations]), 200
  except Exception as e:
    return jsonify({
      'error': str(e)
    }), 400