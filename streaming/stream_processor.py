from typing import Dict, Any
from datetime import datetime

from detection.preprocessor import preprocess_input 
from app.services.detection_service import DetectionService
from app.services.alert_service import AlertService
from database.crud import insert_log  


class StreamProcessor:
    """
    Processes real-time network traffic stream
    """

    def __init__(self):
        self.detector = DetectionService()
        self.alert_service = AlertService()

    # =========================
    # PROCESS SINGLE EVENT
    # =========================
    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:

        try:
            # -------------------------
            # PREPROCESS INPUT
            # -------------------------
            clean_data = preprocess_input(event)

            # -------------------------
            # DETECTION
            # -------------------------
            result = self.detector.detect(clean_data)   # ✅ FIXED (detect, not predict)

            prediction = result.get("prediction", "unknown")
            confidence = result.get("confidence", 0)

            timestamp = datetime.utcnow()

            # -------------------------
            # STORE LOG (FIXED)
            # -------------------------
            insert_log({
                "protocol_type": clean_data.get("protocol_type"),
                "service": clean_data.get("service"),
                "flag": clean_data.get("flag"),
                "src_bytes": clean_data.get("src_bytes"),
                "dst_bytes": clean_data.get("dst_bytes"),

                "attack_type": prediction,
                "confidence": confidence,
                "severity": "HIGH" if prediction != "normal" else "LOW",
                "event_type": "network",
                "timestamp": timestamp
            })

            # -------------------------
            # ALERT GENERATION
            # -------------------------
            if self._is_threat(prediction):
                self.alert_service.trigger_alert({
                    "attack_type": prediction,
                    "severity": "HIGH",
                    "message": "Intrusion detected",
                    "timestamp": timestamp
                })

            # -------------------------
            # FINAL RESPONSE
            # -------------------------
            return {
                "attack_type": prediction,
                "confidence": confidence,
                "timestamp": timestamp.isoformat()
            }

        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    # =========================
    # THREAT CHECK
    # =========================
    def _is_threat(self, prediction: str) -> bool:
        return str(prediction).lower() != "normal"

    # =========================
    # STREAM HANDLER
    # =========================
    def handle_stream(self, event_stream):
        print("📡 Stream processing started...")

        for event in event_stream:
            result = self.process_event(event)
            self._print_result(result)

    # =========================
    # OUTPUT (DEBUG)
    # =========================
    def _print_result(self, result):
        if "error" in result:
            print(f" Error: {result['error']}")
            return

        print(
            f"[{result['timestamp']}] "
            f"Attack: {result.get('attack_type')} | "
            f"Confidence: {result.get('confidence')}%"
        )
