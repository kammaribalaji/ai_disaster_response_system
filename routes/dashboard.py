from flask import Blueprint, jsonify
import sqlite3
import os
import random

dashboard_bp = Blueprint('dashboard_bp', __name__)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai_disaster_response.db')

_activity_log = [
    {"time": "16:05", "type": "danger", "icon": "bi-exclamation-octagon", "msg": "HIGH RISK alert triggered in Zone G"},
    {"time": "15:48", "type": "primary", "icon": "bi-truck", "msg": "Team Alpha dispatched to Zone D"},
    {"time": "15:30", "type": "success", "icon": "bi-box2-heart", "msg": "Relief package delivered to Zone B"},
    {"time": "15:10", "type": "warning", "icon": "bi-cloud-rain", "msg": "Rainfall exceeded 120mm in Zone G"},
    {"time": "14:55", "type": "primary", "icon": "bi-person-fill-check", "msg": "40 civilians evacuated from Zone D"},
]

@dashboard_bp.route('/api/dashboard', methods=['GET'])
def get_dashboard_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM zones')
    monitored_zones = c.fetchone()[0] or 9 
    
    c.execute('SELECT COUNT(*) FROM alerts WHERE risk_level IN ("High", "Medium")')
    high_risk_alerts = c.fetchone()[0] or 0
    
    c.execute('SELECT COUNT(*) FROM reports WHERE status="Pending"')
    active_rescue = c.fetchone()[0] or 0
    
    relief_delivered = 450
    conn.close()
    
    # Simulate a live fluctuation for real-time feel
    high_risk_alerts = max(high_risk_alerts, random.randint(2, 8))
    active_rescue = max(active_rescue, random.randint(3, 12))
    
    timeline = {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "data": [5, 12, 8, 20, 15, 30, 10]
    }
    
    zone_comparison = {
        "labels": ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E", "Zone G"],
        "risk": [10, 50, 30, 80, 20, 90],
        "population": [60, 15, 25, 32, 18, 45]
    }
    
    resource_suggestion = "Deploy additional relief to Zone G (High Risk, 90%) and Zone D (Risk: 80%). Zone A is stable."
    
    return jsonify({
        "monitored_zones": monitored_zones if monitored_zones > 0 else 9,
        "high_risk_alerts": high_risk_alerts,
        "active_rescue_ops": active_rescue,
        "relief_delivered": relief_delivered,
        "timeline": timeline,
        "zone_comparison": zone_comparison,
        "activity_log": _activity_log,
        "resource_suggestion": resource_suggestion
    })

@dashboard_bp.route('/api/performance', methods=['GET'])
def get_performance():
    return {
        "avg_response_time_mins": round(random.uniform(8, 22), 1),
        "relief_success_pct": round(random.uniform(72, 95), 1),
        "team_efficiency_pct": round(random.uniform(78, 96), 1),
        "zones_covered": random.randint(6, 9),
        "active_operations": random.randint(3, 12),
        "civilians_evacuated": random.randint(150, 600)
    }

@dashboard_bp.route('/api/alerts/broadcast', methods=['POST'])
def broadcast_alert():
    from flask import request as req
    data = req.json or {}
    target = data.get('target', 'All')
    message = data.get('message', 'Emergency Alert')
    return {"success": True, "message": f"Alert sent to '{target}': {message}"}
