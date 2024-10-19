from flask import Blueprint, request, jsonify
from src.usecases import VolunteerUseCase

delete_reservation_bp = Blueprint('delete_reservation', __name__)

@delete_reservation_bp.route('/volunteer/delete_reservation', methods=['POST'])
def delete_reservation():
    """Delete reservation
    ---
    parameters:
        - name: reservation_id
          in: query
          type: int
          required: true
    ---
    responses:
        200:
            description: Reservation deleted
        400:
            description: Reservation not deleted
    """
    
    reservation_id = request.args.get('reservation_id')
    use_case = VolunteerUseCase()
    try:
        use_case.delete_reservation(reservation_id)
        return jsonify({
            'message': 'Reservation deleted'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400