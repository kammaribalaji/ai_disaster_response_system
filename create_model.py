"""
Train and save ML model for disaster prediction
This script creates a simple mock model for demo purposes
"""

import pickle
import os
import numpy as np

class DisasterPredictionModel:
    """Simple mock model for disaster risk prediction"""
    
    def __init__(self):
        # Feature names
        self.feature_names = ['rainfall', 'wind_speed', 'river_level', 'humidity', 'temperature', 'pressure']
        
        # Model weights (for demo - these are hardcoded thresholds)
        self.thresholds = {
            'rainfall': 100,
            'wind_speed': 60,
            'river_level': 5,
            'humidity': 85,
            'temperature': 35,
            'pressure': 950
        }
    
    def predict(self, X):
        """Predict disaster risk level (0: Low, 1: Medium, 2: High)"""
        predictions = []
        
        for features in X:
            risk_score = 0
            
            # Rainfall effect
            if features[0] > self.thresholds['rainfall']:
                risk_score += 2
            elif features[0] > self.thresholds['rainfall'] * 0.7:
                risk_score += 1
            
            # Wind speed effect
            if features[1] > self.thresholds['wind_speed']:
                risk_score += 2
            elif features[1] > self.thresholds['wind_speed'] * 0.7:
                risk_score += 1
            
            # River level effect
            if features[2] > self.thresholds['river_level']:
                risk_score += 2
            
            # Classify
            if risk_score >= 4:
                predictions.append(2)  # High risk
            elif risk_score >= 2:
                predictions.append(1)  # Medium risk
            else:
                predictions.append(0)  # Low risk
        
        return np.array(predictions)
    
    def predict_proba(self, X):
        """Predict probabilities for each class"""
        predictions = self.predict(X)
        proba = np.zeros((len(predictions), 3))
        
        for i, pred in enumerate(predictions):
            # Set high probability for predicted class, low for others
            proba[i] = [0.1, 0.3, 0.6] if pred == 2 else [0.4, 0.4, 0.2] if pred == 1 else [0.7, 0.2, 0.1]
        
        return proba

def train_and_save_model():
    """Create and save the disaster prediction model"""
    
    # Create model
    model = DisasterPredictionModel()
    
    # Create model directory if it doesn't exist
    model_dir = os.path.join(os.path.dirname(__file__), 'model')
    os.makedirs(model_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(model_dir, 'model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"✓ Model created and saved to {model_path}")
    return model_path

if __name__ == '__main__':
    train_and_save_model()
