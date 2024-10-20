from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
from ..services import is_valid_timestamp

update_walking_schedule_bp = Blueprint('update_walking_schedule', __name__)
@update_walking_schedule_bp.route('/caretaker/update_walking_schedule', methods=['PUT'])
def update_walking_schedule():
  """
  Update walking schedule.
  ---
  parameters:
    - name: walking_schedule_id
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
      description: Updated
    400:
      description: Invalid input      
  """


  walking_schedule_id = request.args.get('walking_schedule_id')
  start_time = request.args.get('start_time')
  end_time = request.args.get('end_time')

  if not is_valid_timestamp(start_time) or not is_valid_timestamp(end_time):
    return jsonify({
      'error': 'Invalid date time',
      'start_time': start_time,
      'end_time': end_time
    }), 400

  use_case = CaretakerUseCase()
  try:
    use_case.update_walking_schedule(walking_schedule_id, start_time, end_time)
    return jsonify({'message': 'Walking schedule updated'}), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 400
