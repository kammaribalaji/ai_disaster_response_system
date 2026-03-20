import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

def generate_mock_data(n_samples=2000):
    np.random.seed(42)
    # Generate features
    rainfall = np.random.uniform(0, 300, n_samples)
    wind_speed = np.random.uniform(0, 150, n_samples)
    river_level = np.random.uniform(0, 15, n_samples)
    humidity = np.random.uniform(20, 100, n_samples)
    temperature = np.random.uniform(10, 45, n_samples)
    pressure = np.random.uniform(980, 1030, n_samples)
    
    # Calculate a risk score
    risk_score = (rainfall * 0.4) + (wind_speed * 0.3) + (river_level * 10) + ((1030 - pressure) * 2)
    
    # Classify into 0: Low, 1: Medium, 2: High
    risk_level = []
    for score in risk_score:
        if score < 150:
            risk_level.append(0)
        elif score < 250:
            risk_level.append(1)
        else:
            risk_level.append(2)
            
    df = pd.DataFrame({
        'rainfall': rainfall,
        'wind_speed': wind_speed,
        'river_level': river_level,
        'humidity': humidity,
        'temperature': temperature,
        'pressure': pressure,
        'risk_level': risk_level
    })
    return df

def train():
    print("Generating mock data...")
    df = generate_mock_data()
    
    X = df.drop('risk_level', axis=1)
    y = df['risk_level']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"Model Accuracy: {score:.2f}")
    
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train()
