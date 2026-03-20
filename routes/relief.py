from flask import Blueprint, jsonify, request
from services.relief_service import get_relief_priority
from services.simulation_service import trigger_simulation

relief_bp = Blueprint('relief_bp', __name__)

@relief_bp.route('/api/relief-priority', methods=['GET'])
def relief_priority():
    result = get_relief_priority()
    return jsonify({"priorities": result})

@relief_bp.route('/api/simulate', methods=['POST'])
def run_simulation():
    result = trigger_simulation()
    return jsonify(result)
