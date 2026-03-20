import sqlite3
import os
import random
from services.ml_service import predict_risk

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai_disaster_response.db')

def trigger_simulation():
    zones = ['Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E', 'Zone F', 'Zone G', 'Zone H', 'Zone I']
    simulations = []
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    for i in range(3):
        zone = random.choice(zones)
        data = {
            'rainfall': random.uniform(50, 250),
            'wind_speed': random.uniform(20, 120),
            'river_level': random.uniform(2, 12),
            'humidity': random.uniform(40, 95),
            'temperature': random.uniform(15, 35),
            'pressure': random.uniform(990, 1020)
        }
        
        result = predict_risk(data)
        
        if "error" not in result:
            c.execute('''
                INSERT INTO alerts (zone, risk_level, message)
                VALUES (?, ?, ?)
            ''', (zone, result['risk_level'], result['explanation']))
            
            simulations.append({
                "zone": zone,
                "risk_level": result['risk_level'],
                "explanation": result['explanation']
            })
            
    conn.commit()
    conn.close()
    
    return {"status": "success", "events": simulations}
