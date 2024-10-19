from flask import Blueprint, request, jsonify
from src.usecases import VeterinarianUseCase
from ..services import is_valid_timestamp

schedule_request_bp = Blueprint('schedule_request', __name__)
@schedule_request_bp.route('/veterinarian/schedule_request', methods=['POST'])

def schedule_request():
  """
  Schedule a request from a caretaker.
  ---
  parameters:
    - name: request_id
      in: query
      required: true
      type: integer
    - name: date_time
      in: query
      required: true
      type: string
    - name: status
      in: query
      required: true
      type: string
  responses:
    200:
      description: Request successfully scheduled
    400:
      description: Request could not be scheduled
  """
  use_case = VeterinarianUseCase()
  
  request_id = request.args.get('request_id')
  date_time = request.args.get('date_time')
  status = request.args.get('status')
  if not is_valid_timestamp(date_time):
    return jsonify({
      'error': 'Invalid date time'
    }), 400
  try:
    scheduled_request = use_case.schedule_request(request_id, date_time, status)
    return jsonify({
      'id': scheduled_request.id,
      'date_time': scheduled_request.date_time,
      'status': scheduled_request.status
    }), 200    
  except Exception as e:
    return jsonify({
      'error': str(e)
    }), 400
  