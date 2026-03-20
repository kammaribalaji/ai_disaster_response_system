from flask import Blueprint, request, jsonify
from services.ml_service import predict_risk

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    if not data:
        return jsonify({"error": "No input data"}), 400
    result = predict_risk(data)
    return jsonify(result)
