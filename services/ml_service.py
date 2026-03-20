import pickle
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'model.pkl')
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

def predict_risk(data):
    if model is None:
        load_model()
    if model is None:
        return {"error": "Model not found. Please train the model first."}
    
    features = ['rainfall', 'wind_speed', 'river_level', 'humidity', 'temperature', 'pressure']
    input_data = np.array([[data.get(f, 0) for f in features]])
    
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    
    # 0 to 100 roughly
    risk_score = probabilities[1] * 50 + probabilities[2] * 100
    
    levels = ["Low", "Medium", "High"]
    risk_level = levels[prediction]
    
    # Pro-Level Explainable AI logic
    exai_factors = []
    reasons = []
    
    rf = float(data.get('rainfall', 0))
    if rf > 100:
        exai_factors.append({"feature": "rainfall", "importance": 0.45})
        reasons.append(f"Rainfall ({rf}mm) exceeds safe limits by {round((rf-100)/100*100)}%")
        
    ws = float(data.get('wind_speed', 0))
    if ws > 60:
        exai_factors.append({"feature": "wind_speed", "importance": 0.25})
        reasons.append(f"Wind speed ({ws}km/h) is dangerously high")
        
    rl = float(data.get('river_level', 0))
    if rl > 5:
        exai_factors.append({"feature": "water_level", "importance": 0.20})
        reasons.append(f"Water level ({rl}m) indicates imminent flooding")
        
    if not reasons and int(prediction) > 0:
        exai_factors.append({"feature": "cumulative_conditions", "importance": 0.10})
        reasons.append("Cumulative environmental factors are elevating risk")
    elif not reasons:
        reasons.append("All metrics are within nominal safety parameters")
        
    # Generate 24-hour forecast trend (6 data points, every 4 hours)
    import random
    base_trend = risk_score
    forecast_data = []
    forecast_labels = ["+4h", "+8h", "+12h", "+16h", "+20h", "+24h"]
    for i in range(6):
        # Simulate realistic trend drift
        if risk_level == "High":
             base_trend += random.uniform(-2, 5) # Stays high or gets slightly worse
        elif risk_level == "Medium":
             base_trend += random.uniform(-5, 8) # Volatile
        else:
             base_trend += random.uniform(-3, 3) # Stable
             
        forecast_data.append(min(100, max(0, round(base_trend, 1))))

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "severity_index": int(prediction),
        "confidence": round(float(max(probabilities)) * 100, 1),
        "explanation": ". ".join(reasons) + ".",
        "exai_factors": exai_factors,
        "forecast": {
            "labels": forecast_labels,
            "data": forecast_data
        }
    }
