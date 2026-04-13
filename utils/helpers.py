import numpy as np

# INTERPRET MODEL OUTPUT

def interpret_result(prediction, encoder=None):
    """
    Convert model prediction → human-readable label
    """
    try:
        if encoder:
            return encoder.inverse_transform([prediction])[0]
        return str(prediction)
    except Exception:
        return "unknown"


# CONFIDENCE SCORE

def confidence_score(model, features):
    """
    Get confidence score (percentage)
    """
    try:
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(features)
            confidence = np.max(probs) * 100
            return round(confidence, 2)
        return None
    except Exception:
        return None


# SEVERITY CLASSIFICATION

def classify_severity(attack_type: str, confidence: float) -> str:
    """
    Classify alert severity
    """
    attack_type = str(attack_type).lower()

    if attack_type == "normal":
        return "low"

    if confidence >= 85:
        return "high"
    elif confidence >= 60:
        return "medium"
    else:
        return "low"

# GENERATE ALERT MESSAGE

def generate_alert_message(attack_type: str, confidence: float) -> str:
    """
    Create human-readable alert message
    """
    return (
        f" Detected {attack_type.upper()} attack "
        f"with {confidence}% confidence"
    )


# SAFE FLOAT CONVERSION

def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default

# NORMALIZE INPUT DATA

def normalize_input(data: dict) -> dict:
    """
    Ensure all numeric values are safe
    """
    normalized = {}

    for key, value in data.items():
        if isinstance(value, (int, float)):
            normalized[key] = value
        else:
            try:
                normalized[key] = float(value)
            except Exception:
                normalized[key] = value

    return normalized
