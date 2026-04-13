import os
import json
from datetime import datetime
from flask import current_app


class AlertService:
    """
    Handles alert generation and notification logic
    """

    def __init__(self):
        self.alert_threshold = 70  # confidence threshold
        self.alert_log_file = self._get_alert_log_path()

    # ALERT TRIGGER
  
    def evaluate_and_alert(self, result: dict, input_data: dict):
        """
        Evaluate detection result and trigger alert if needed
        """
        try:
            if not result or result.get("label") == "Error":
                return

            label = result.get("label")
            confidence = result.get("confidence", 0)

            # Trigger alert if attack detected
            if label == "Attack" and confidence >= self.alert_threshold:
                alert_data = self._build_alert(result, input_data)

                # Log alert
                self._log_alert(alert_data)

                # Future: send email / webhook
                self._notify(alert_data)

        except Exception as e:
            current_app.logger.error(f"[ALERT ERROR] {str(e)}")

    # BUILD ALERT

    def _build_alert(self, result, input_data):
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "severity": self._get_severity(result.get("confidence")),
            "attack_type": result.get("attack_type"),
            "confidence": result.get("confidence"),
            "input": input_data
        }

    # SEVERITY LEVEL
  
    def _get_severity(self, confidence):
        if confidence >= 90:
            return "HIGH"
        elif confidence >= 75:
            return "MEDIUM"
        else:
            return "LOW"

    # LOG ALERT
  
    def _log_alert(self, alert_data):
        try:
            os.makedirs(os.path.dirname(self.alert_log_file), exist_ok=True)

            with open(self.alert_log_file, "a") as f:
                f.write(json.dumps(alert_data) + "\n")

        except Exception as e:
            current_app.logger.error(f"[ALERT LOG ERROR] {str(e)}")

    # NOTIFICATION 
  
    def _notify(self, alert_data):
        """
        Extend this method for:
        - Email alerts
        - Slack notifications
        - Webhooks
        """
        try:
            # For now, just log to console
            current_app.logger.warning(
                f"[ALERT] {alert_data['severity']} threat detected: "
                f"{alert_data['attack_type']} ({alert_data['confidence']}%)"
            )

        except Exception as e:
            current_app.logger.error(f"[ALERT NOTIFY ERROR] {str(e)}")

    # GET ALERT LOG PATH
    
    def _get_alert_log_path(self):
        try:
            config = current_app.config if current_app else None

            if config:
                log_dir = config.get("LOG_DIR", "logs")
            else:
                log_dir = "logs"

            return os.path.join(log_dir, "alerts.log")

        except:
            return "logs/alerts.log"
