from flask import Blueprint, request, jsonify, current_app
from app.services.detection_service import DetectionService
from app.services.logging_service import log_event

# Create Blueprint
detection_bp = Blueprint("detection", __name__)

# Initialize service
detector = DetectionService()


@detection_bp.route("/", methods=["POST"])
def detect_intrusion():
    """
    Detect intrusion from incoming network data
    """
    try:
        data = request.get_json()

        # VALIDATION
      
        if not data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        if not isinstance(data, dict):
            return jsonify({
                "status": "error",
                "message": "Invalid input format (JSON required)"
            }), 400

        
        # DETECTION
        
        result = detector.predict(data)

        
        # LOG EVENT
        
        log_event(
            event_type="DETECTION",
            data=data,
            result=result
        )

        # RESPONSE
        
        return jsonify({
            "status": "success",
            "prediction": result.get("label"),
            "confidence": result.get("confidence"),
            "attack_type": result.get("attack_type"),
            "timestamp": result.get("timestamp")
        }), 200

    except Exception as e:
        current_app.logger.error(f"[DETECTION ERROR] {str(e)}")

        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500


@detection_bp.route("/health", methods=["GET"])
def detection_health():
    """
    Health check for detection service
    """
    return jsonify({
        "status": "ok",
        "service": "detection"
    }), 200
