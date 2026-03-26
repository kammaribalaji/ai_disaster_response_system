from flask import Blueprint, jsonify, render_template, redirect, url_for, abort
import sqlite3
import os
from auth import get_current_user, login_required

map_bp = Blueprint('map_bp', __name__)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai_disaster_response.db')

@map_bp.route('/map')
@login_required
def map_page():
    """Telangana Disaster Map - Real-time disaster visualization (Admin & Rescue only)"""
    user = get_current_user()
    # Restrict to admin and rescue roles only
    if user['role'] not in ['admin', 'rescue']:
        abort(403)
    return render_template('map.html', user=user)

@map_bp.route('/api/risk-map', methods=['GET'])
def get_risk_map():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT name, lat, lng, base_risk FROM zones')
    zones = [dict(row) for row in c.fetchall()]
    conn.close()
    
    if not zones:
        zones = [
            {"name": "Zone G", "lat": 12.9716, "lng": 77.5946, "base_risk": 90, "population": 45000},
            {"name": "Zone D", "lat": 12.9352, "lng": 77.6245, "base_risk": 80, "population": 32000},
            {"name": "Zone B", "lat": 12.9141, "lng": 77.6308, "base_risk": 50, "population": 15000},
            {"name": "Zone A", "lat": 13.0827, "lng": 80.2707, "base_risk": 10, "population": 60000}
        ]
        
    # Mock Pro-Level Data for Layers
    shelters = [
        {"name": "Central High School Shelter", "lat": 12.9700, "lng": 77.5900, "capacity": 500, "occupancy": 320},
        {"name": "Community Hall Refuge", "lat": 12.9150, "lng": 77.6320, "capacity": 200, "occupancy": 190},
        {"name": "North Stadium Safe Zone", "lat": 13.0850, "lng": 80.2750, "capacity": 1500, "occupancy": 450}
    ]
    
    rescue_teams = [
        {"id": "Team Alpha (Boats)", "lat": 12.9730, "lng": 77.5960, "status": "Active Rescue"},
        {"id": "Team Bravo (Medics)", "lat": 12.9340, "lng": 77.6260, "status": "En Route"},
        {"id": "Air Unit 1", "lat": 13.0800, "lng": 80.2600, "status": "Patrol"}
    ]
    
    return jsonify({
        "zones": zones,
        "shelters": shelters,
        "rescue_teams": rescue_teams
    })
