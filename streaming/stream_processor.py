from typing import Dict, Any
from datetime import datetime
from detection.preprocessor import preprocess_input
from app.services.detection_service import DetectionService                                                    
from app.services.alert_service import AlertService
from app.services.logging_service import log_event


class StreamProcessor:
    """
    Processes real-time network traffic stream
    """

    def __init__(self):
        self.detector = DetectionService()
        self.alert_service = AlertService()

    # PROCESS SINGLE EVENT
    
    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full pipeline for one network event
        """

        try:
    
            # PREPROCESS INPUT

            clean_data = preprocess_input(event)

            # DETECTION

            result = self.detector.predict(clean_data)

            # ADD METADATA
    
            result["timestamp"] = datetime.utcnow().isoformat()

            # LOG EVENT

            log_event(
                event_type="network_traffic",
                data=clean_data,
                result=result
            )

            # ALERT GENERATION
    
            if self._is_threat(result):
                self.alert_service.trigger_alert(result)

            return result

        except Exception as e:
            error_result = {
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

            # Log error
            log_event(
                event_type="processing_error",
                data=event,
                result=error_result
            )

            return error_result

    # THREAT CHECK
  
    def _is_threat(self, result: Dict[str, Any]) -> bool:
        """
        Decide whether this is an attack
        """
        label = str(result.get("attack_type", "")).lower()

        return label != "normal"

    # STREAM HANDLER

    def handle_stream(self, event_stream):
        """
        Process continuous stream (generator)
        """
        print("📡 Stream processing started...")

        for event in event_stream:
            result = self.process_event(event)

            # Optional: print or push to dashboard
            self._print_result(result)

    # OUTPUT (DEBUG / MONITORING)
  
    def _print_result(self, result):
        if "error" in result:
            print(f" Error: {result['error']}")
            return

        print(
            f"[{result['timestamp']}] "
            f"Attack: {result.get('attack_type')} | "
            f"Confidence: {result.get('confidence')}%"
                     )
