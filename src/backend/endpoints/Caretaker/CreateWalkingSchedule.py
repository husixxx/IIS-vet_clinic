from flask import Blueprint, request, jsonify
from backend import CaretakerUseCase

create_walking_schedule_bp = Blueprint('create_walking_schedule', __name__)


@create_walking_schedule_bp.route('/caretaker/walking_schedule', methods=['POST'])
def create_walking_schedule():
    """Create a walking schedule
    ---
    parameters:
      - name: animal_id
        in: query
        type: integer
        required: true
      - name: volunteer_id
        in: query
        type: integer
        required: true
      - name: start_time
        in: query
        type: string
        required: true
      - name: end_time
        in: query
        type: string
        required: true
      - name: status
        in: query
        type: string
        required: true
    responses:
      200:
        description: Walking schedule created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            animal_id:
              type: integer
            volunteer_id:
              type: integer
            start_time:
              type: string
            end_time:
              type: string
            status:
              type: string
      400:
        description: Invalid input
    """
    
    
    animal_id = request.args.get('animal_id', type=int)
    volunteer_id = request.args.get('volunteer_id', type=int)
    start_time = request.args.get('start_time', type=str)
    end_time = request.args.get('end_time', type=str)
    status = request.args.get('status', type=str)


    caretaker_use_case = CaretakerUseCase()
    walking_schedule = caretaker_use_case.create_walking_schedule(animal_id, volunteer_id, start_time, end_time, status)

    return {
        'id': walking_schedule.id,
        'animal_id': walking_schedule.animal_id,
        'volunteer_id': walking_schedule.volunteer_id,
        'start_time': walking_schedule.start_time,
        'end_time': walking_schedule.end_time,
        'status': walking_schedule.status
    }, 200
