from flask import Blueprint, request, jsonify
from services.dijkstra_service import calculate_route

route_bp = Blueprint('route_bp', __name__)

@route_bp.route('/api/route', methods=['GET', 'POST'])
def get_route():
    if request.method == 'POST':
        data = request.json or {}
        start_val = data.get('start', 'A')
        end_val = data.get('end', 'I')
    else:
        start_val = request.args.get('start', 'A')
        end_val = request.args.get('end', 'I')
        
    start = f"Zone {start_val}" if not start_val.startswith("Zone") else start_val
    end = f"Zone {end_val}" if not end_val.startswith("Zone") else end_val
    
    result = calculate_route(start, end)
    return jsonify(result)
