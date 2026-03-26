from flask import Blueprint, jsonify, request, render_template
from services.relief_service import get_relief_priority
from services.simulation_service import trigger_simulation
from auth import get_current_user, login_required

relief_bp = Blueprint('relief_bp', __name__)

@relief_bp.route('/relief')
@login_required
def relief_page():
    """Relief distribution and centers management"""
    user = get_current_user()
    return render_template('relief.html', user=user)

@relief_bp.route('/api/relief-priority', methods=['GET'])
def relief_priority():
    result = get_relief_priority()
    return jsonify({"priorities": result})

@relief_bp.route('/api/simulate', methods=['POST'])
def run_simulation():
    result = trigger_simulation()
    return jsonify(result)
