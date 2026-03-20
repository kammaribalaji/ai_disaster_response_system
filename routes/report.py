from flask import Blueprint, request, jsonify
import sqlite3, os, random

report_bp = Blueprint('report_bp', __name__)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai_disaster_response.db')

# Mock in-memory reports for demo
_reports = [
    {"id": 1, "name": "Ravi Kumar", "zone": "Zone G", "location": "Block 4, Zone G", "lat": 12.971, "lng": 77.594, "urgency": "urgent", "status": "Pending", "time": "16:05", "description": "Family trapped on rooftop, water rising fast", "image": None},
    {"id": 2, "name": "Priya Sharma", "zone": "Zone D", "location": "Market Street, Zone D", "lat": 12.935, "lng": 77.624, "urgency": "urgent", "status": "In Progress", "time": "15:48", "description": "Elderly person needs medical assistance urgently", "image": None},
    {"id": 3, "name": "Amit Singh", "zone": "Zone B", "location": "River Road, Zone B", "lat": 12.914, "lng": 77.630, "urgency": "normal", "status": "Pending", "time": "15:30", "description": "Road completely flooded, vehicles stranded", "image": None},
    {"id": 4, "name": "Lakshmi R.", "zone": "Zone G", "location": "Temple Street, Zone G", "lat": 12.972, "lng": 77.593, "urgency": "urgent", "status": "Resolved", "time": "14:55", "description": "10 children need immediate evacuation", "image": None},
    {"id": 5, "name": "Mohan Das", "zone": "Zone A", "location": "Park Area, Zone A", "lat": 13.082, "lng": 80.270, "urgency": "normal", "status": "Pending", "time": "14:20", "description": "Tree fallen blocking main road", "image": None},
]
_next_id = 6

@report_bp.route('/api/report', methods=['POST'])
def submit_report():
    global _next_id
    data = request.json or {}
    if 'description' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    report = {
        "id": _next_id,
        "name": data.get("name", "Anonymous"),
        "zone": data.get("zone", "Unknown Zone"),
        "location": data.get("location", ""),
        "lat": data.get("lat", 0.0),
        "lng": data.get("lng", 0.0),
        "urgency": data.get("severity", "normal").lower(),
        "status": "Pending",
        "time": data.get("time", "Now"),
        "description": data.get("description", ""),
        "image": data.get("image", None)
    }
    _reports.append(report)
    _next_id += 1

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO reports (location, lat, lng, description, severity, status)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (report['location'], report['lat'], report['lng'],
                   report['description'], data.get('severity', 'Medium'), 'Pending'))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return jsonify({"status": "success", "report_id": report['id']}), 201

@report_bp.route('/api/reports', methods=['GET'])
def get_reports():
    f = request.args.get('filter', 'all')
    if f == 'urgent':
        data = [r for r in _reports if r['urgency'] == 'urgent']
    elif f == 'pending':
        data = [r for r in _reports if r['status'] == 'Pending']
    elif f == 'resolved':
        data = [r for r in _reports if r['status'] == 'Resolved']
    else:
        data = _reports
    return jsonify(data)

@report_bp.route('/api/reports/<int:report_id>/assign', methods=['POST'])
def assign_report(report_id):
    data = request.json or {}
    for r in _reports:
        if r['id'] == report_id:
            r['status'] = data.get('status', 'In Progress')
            return jsonify({"success": True, "report": r})
    return jsonify({"error": "Report not found"}), 404
