from flask import Blueprint, request, jsonify

chat_bp = Blueprint('chat_bp', __name__)

# Pre-defined AI response rules
RULES = [
    (["risky", "dangerous", "risk", "high risk"], "The highest risk zones right now are Zone G (90% risk) and Zone D (80% risk). Immediate evacuation is recommended for Zone G."),
    (["shelter", "safe", "refuge", "nearest shelter", "safety"], "There are 3 active shelters: Central High School (320/500), Community Hall (190/200), and North Stadium (450/1500). North Stadium has the most space."),
    (["flood", "flooding", "water level", "water"], "Flood warnings are active for Zone G and Zone D. River levels have exceeded 5m. Avoid low-lying areas."),
    (["team", "rescue team", "help", "who is helping"], "3 rescue units are deployed: Team Alpha (Boats) in Zone G, Team Bravo (Medics) heading to Zone D, and Air Unit 1 on patrol."),
    (["rain", "rainfall", "storm", "cyclone", "how bad"], "Rainfall in Zone G has exceeded 120mm — 35% above the danger threshold. Storm conditions are expected for the next 12 hours."),
    (["evacuate", "leave", "escape", "evacuation"], "Please evacuate Zone G and Zone D immediately. Move to North Stadium Shelter. Rescue teams are guiding civilians along Route: Zone D → Zone C → Zone A."),
    (["supply", "food", "relief", "medicine", "resources"], "Relief has been delivered to Zone B and Zone A. Zone D and Zone G are still waiting for supplies. Priority dispatch is in progress."),
    (["predict", "prediction", "forecast", "risk score"], "Based on current data, Zone G has a 90% risk score with a HIGH risk prediction for the next 24 hours. Use the AI Risk Check page for a custom analysis."),
]

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    query = data.get('message', '').lower().strip()
    
    if not query:
        return jsonify({"reply": "Please ask a question about the disaster situation."})
    
    # Rule-based matching
    for keywords, response in RULES:
        if any(kw in query for kw in keywords):
            return jsonify({"reply": response})
    
    # Fallback
    return jsonify({
        "reply": "I'm not sure about that. You can ask me about: risky zones, nearby shelters, evacuation routes, rescue teams, rainfall levels, or relief supplies."
    })
