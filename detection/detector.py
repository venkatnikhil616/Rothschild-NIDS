import os
import pickle
import numpy as np
from typing import Any, Dict, Optional

from detection.feature_extractor import extract_features

class Detector:
    """
    Low-level ML inference engine.
    Responsible ONLY for:
    - Loading model artifacts
    - Running predictions
    - Returning raw outputs
    """

    def __init__(
        self,
        model_path: str,
        scaler_path: Optional[str] = None,
        encoder_path: Optional[str] = None
    ):
        self.model = None
        self.scaler = None
        self.encoder = None

        self._load_model(model_path)
        self._load_scaler(scaler_path)
        self._load_encoder(encoder_path)
      
    # LOAD MODEL
  
    def _load_model(self, path: str):
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                self.model = pickle.load(f)
        else:
            raise FileNotFoundError(f"Model not found at {path}")

    # LOAD SCALER
  
    def _load_scaler(self, path: Optional[str]):
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                self.scaler = pickle.load(f)

    # ---------------------------
    # LOAD ENCODER
    # ---------------------------
    def _load_encoder(self, path: Optional[str]):
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                self.encoder = pickle.load(f)

    # RUN INFERENCE
  
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform prediction on input data
        """
        if self.model is None:
            raise RuntimeError("Model is not loaded")

        # FEATURE EXTRACTION
      
        features = extract_features(input_data)
        features = np.array(features).reshape(1, -1)

        # SCALING

        if self.scaler:
            features = self.scaler.transform(features)

        # PREDICTION
  
        prediction = self.model.predict(features)[0]

        confidence = self._get_confidence(features)

        attack_type = self._decode_label(prediction)

        return {
            "prediction": prediction,
            "attack_type": attack_type,
            "confidence": confidence
        }

    # CONFIDENCE SCORE

    def _get_confidence(self, features) -> Optional[float]:
        try:
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(features)[0]
                return round(float(np.max(probs)) * 100, 2)
            return None
        except Exception:
            return None

    # LABEL DECODING
  
    def _decode_label(self, prediction) -> str:
        try:
            if self.encoder:
                return self.encoder.inverse_transform([prediction])[0]
            return str(prediction)
        except Exception:
            return str(prediction)
