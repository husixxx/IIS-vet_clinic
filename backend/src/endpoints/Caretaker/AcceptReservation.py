from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

accept_reservation_bp = Blueprint('accept_reservation', __name__)

@accept_reservation_bp.route('/caretaker/accept_reservation', methods=['POST'])
def accept_reservation():
    """Accept a reservation
    ---
    parameters:
      - name: id 
        required: true
        type: int
        in: query
    responses:
      200:
        description: Request accepted
      400:
        description: Request not found/Request already accepted. 
    """
    
    
    id = request.args.get('id')
    use_case = CaretakerUseCase()
    try:
      request = use_case.accept_reservation(id)
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