from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

change_reservation_status_bp = Blueprint('change_reservation_status', __name__)

@change_reservation_status_bp.route('/caretaker/change_reservation_status', methods=['POST'])
def change_reservation_status():
    """Change a reservation status
    ---
    parameters:
      - name: id 
        required: true
        type: int
        in: query
      - name: status 
        required: true
        type: string
        in: query
    responses:
      200:
        description: Request accepted
      400:
        description: Request not found. 
    """
    
    
    id = request.args.get('id')
    status = request.args.get('status')
    use_case = CaretakerUseCase()
    try:
      request = use_case.change_reservation_status(id, status)
      return jsonify({
        'id': request.id,
        'status': request.status,
        'volunteer_id': request.volunteer_id,
        'animal_id': request.animal_id
      })
    except Exception as e:
      return jsonify({
        'error': str(e)
      }), 400