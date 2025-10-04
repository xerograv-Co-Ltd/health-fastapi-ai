# models/predict_engine.py
import joblib
import numpy as np
import os

class PredictEngine:
    def __init__(self, model_path="risk_model.pkl"):
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model file not found.")
        self.model = joblib.load(model_path)

    def predict(self, heart_rate, oxygen_saturation, temperature, depth, max_percent_m):
        # 欠損値には0を入れる（学習時と一致）
        features = np.array([[heart_rate or 0, oxygen_saturation or 0,
                              temperature or 0, depth or 0, max_percent_m or 0]])
        prediction = self.model.predict(features)[0]
        proba = self.model.predict_proba(features)[0].max()
        return {
            "label": prediction,
            "confidence": round(proba, 3)
        }
