from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase
from flask_login import login_required, current_user

change_reservation_status_bp = Blueprint('change_reservation_status', __name__)

@change_reservation_status_bp.route('/caretaker/change_reservation_status', methods=['POST'])
@login_required
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
    if current_user.role != 'caretaker':
      return jsonify({'error': 'Only caretakers can cancel vet requests'}), 403
    
    reservation_id = request.args.get('id')
    status = request.args.get('status')
    use_case = CaretakerUseCase()
    try:
      reservation = use_case.change_reservation_status(reservation_id=reservation_id, status=status)
      return jsonify({
        'id': reservation.id,
        'status': reservation.status,
        'volunteer_id': reservation.volunteer_id,
        'animal_id': reservation.animal_id
      })
    except Exception as e:
      return jsonify({
        'error': str(e)
      }), 400