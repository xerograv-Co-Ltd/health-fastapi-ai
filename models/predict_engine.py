# モデル定義ファイル: models/predict_engine.py
from joblib import load

class PredictEngine:
    def __init__(self):
        self.model = load("risk_model.pkl")

    def predict(self, heart_rate, oxygen_saturation, temperature, depth, max_percent_m):
        features = [[
            heart_rate or 0,
            oxygen_saturation or 0.0,
            temperature or 0.0,
            depth or 0.0,
            max_percent_m or 0.0
        ]]
        pred_label = self.model.predict(features)[0]
        confidence = self.model.predict_proba(features).max()
        return {
            "label": pred_label,
            "confidence": float(confidence)
        }
