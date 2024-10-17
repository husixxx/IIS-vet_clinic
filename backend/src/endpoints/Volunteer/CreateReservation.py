from flask import Blueprint, request, jsonify
from src.usecases import VolunteerUseCase
from ..services import *
create_reservation_bp = Blueprint('create_reservation', __name__)

@create_reservation_bp.route('/volunteer/reservation', methods=['POST'])
def create_reservation():
  
  """
  Create a new reservation.
  ---
  parameters:
    - name: volunteer_id
      required: true
      type: integer
      in: query
    - name: animal_id
      required: true
      type: integer
      in: query
    - name: start_time
      required: true
      type: string
      in: query
    - name: end_time
      required: true
      type: string
      in: query
  responses:
    200:
      description: Reservation created
    400:
      description: Invalid input
  """

  # Získanie parametrov z requestu
  volunteer_id = request.args.get('volunteer_id', type=int)
  animal_id = request.args.get('animal_id', type=int)
  start_time = request.args.get('start_time')
  end_time = request.args.get('end_time')

  # Vytvorenie use case a rezervácie
  use_case = VolunteerUseCase()
  
  try:
    if not is_valid_date(start_time) or not is_valid_date(end_time):
      raise Exception('Invalid date format.')
    use_case.create_reservation(volunteer_id, animal_id, start_time, end_time)
    return jsonify({'message': 'Reservation created'}), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 400