import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai_disaster_response.db')

def get_relief_priority():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM zones')
    zones = c.fetchall()
    
    if not zones:
        mock_zones = [
            {"name": "Zone G", "base_risk": 90, "population": 5000},
            {"name": "Zone D", "base_risk": 80, "population": 3000},
            {"name": "Zone B", "base_risk": 50, "population": 8000},
            {"name": "Zone A", "base_risk": 10, "population": 2000}
        ]
        zones_data = mock_zones
    else:
        zones_data = [dict(z) for z in zones]
        
    conn.close()
    
    for zone in zones_data:
        risk_score = zone['base_risk'] 
        pop_score = zone['population'] / 100
        zone['priority_score'] = round(risk_score + pop_score, 2)
        
    sorted_zones = sorted(zones_data, key=lambda x: x['priority_score'], reverse=True)
    return sorted_zones
