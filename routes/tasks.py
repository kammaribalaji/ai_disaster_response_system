from flask import Blueprint, request, jsonify
import datetime

tasks_bp = Blueprint('tasks_bp', __name__)

_tasks = [
    {"id": 1, "title": "Evacuate Zone G — Block 4", "priority": "critical", "status": "Pending", "assigned_at": "15:48", "details": "~45 civilians stranded on rooftop. Water rising.", "icon": "bi-person-lines-fill", "zone": "Zone G"},
    {"id": 2, "title": "Medical check at Central Shelter", "priority": "medium", "status": "In Progress", "assigned_at": "14:30", "details": "Provide medical support to evacuees. 3 critical patients.", "icon": "bi-hospital", "zone": "Shelter"},
    {"id": 3, "title": "Deliver supplies — Zone B", "priority": "low", "status": "In Progress", "assigned_at": "13:15", "details": "200 relief packages. Food + Medical kits.", "icon": "bi-box2-heart", "zone": "Zone B"},
    {"id": 4, "title": "Rescue boat deployment — Zone D", "priority": "critical", "status": "Pending", "assigned_at": "16:30", "details": "Deploy rescue boats to Main Bridge area Zone D.", "icon": "bi-water", "zone": "Zone D"},
    {"id": 5, "title": "Search and rescue — Zone G East", "priority": "critical", "status": "Pending", "assigned_at": "16:45", "details": "Multiple families reported trapped. Coordinate with Team Alpha.", "icon": "bi-search-heart", "zone": "Zone G"},
    {"id": 6, "title": "Route scouting — Northern corridor", "priority": "medium", "status": "Completed", "assigned_at": "12:00", "details": "Verified safe path through Zone C to North Stadium.", "icon": "bi-signpost-split", "zone": "Zone C"},
]

_field_updates = []

@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    status_filter = request.args.get('status', 'all')
    if status_filter == 'all':
        return jsonify(_tasks)
    return jsonify([t for t in _tasks if t['status'].lower() == status_filter.lower()])

@tasks_bp.route('/api/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    data = request.json or {}
    for t in _tasks:
        if t['id'] == task_id:
            if 'status' in data:
                t['status'] = data['status']
            return jsonify({"success": True, "task": t})
    return jsonify({"error": "Task not found"}), 404

@tasks_bp.route('/api/sos', methods=['POST'])
def sos():
    data = request.json or {}
    team = data.get('team', 'Unknown Team')
    location = data.get('location', 'Unknown Location')
    message = data.get('message', 'Emergency SOS')
    timestamp = datetime.datetime.now().strftime('%H:%M')
    alert = {
        "type": "SOS",
        "team": team,
        "location": location,
        "message": message,
        "timestamp": timestamp
    }
    return jsonify({"success": True, "alert": alert, "message": f"SOS from {team} received! Admin notified."})

@tasks_bp.route('/api/field-update', methods=['POST'])
def field_update():
    data = request.json or {}
    update = {
        "team": data.get('team', 'Field Team'),
        "zone": data.get('zone', 'Unknown'),
        "message": data.get('message', ''),
        "status": data.get('status', 'update'),
        "timestamp": datetime.datetime.now().strftime('%H:%M'),
        "image": data.get('image', None)
    }
    _field_updates.append(update)
    return jsonify({"success": True, "update": update})

@tasks_bp.route('/api/field-updates', methods=['GET'])
def get_field_updates():
    return jsonify(_field_updates[-20:])  # Last 20 updates

@tasks_bp.route('/api/simulation/status', methods=['GET'])
def simulation_status():
    return jsonify({
        "active": True,
        "scenario": "Cyclone + Flood (Category 3)",
        "hour": 6,
        "flood_spread": [
            {"zone": "Zone G", "spread_pct": 85},
            {"zone": "Zone D", "spread_pct": 62},
            {"zone": "Zone B", "spread_pct": 38},
        ],
        "predicted_peak": "+18h",
        "evacuation_progress": 67
    })
