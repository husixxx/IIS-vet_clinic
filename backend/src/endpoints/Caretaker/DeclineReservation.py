from flask import Blueprint, request, jsonify
from src.usecases import CaretakerUseCase

decline_reservation_bp = Blueprint('decline_reservation', __name__)

@decline_reservation_bp.route('/caretaker/decline_reservation', methods=['POST'])
def decline_reservation():
    """decline a reservation
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
        description: Request not found. 
    """
    
    
    id = request.args.get('id')
    use_case = CaretakerUseCase()
    try:
      request = use_case.decline_reservation(id)
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