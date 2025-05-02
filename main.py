from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    heart_rate: float
    skin_temp: float
    uv_index: float  # unused but included
    pm25: float      # unused but included
    humidity: float  # unused but included
    oxygen_saturation: float
    activity_level: float

@app.post("/analyze")
def analyze(data: InputData):
    # 各要因ごとのスコア
    oxygen_risk = (100 - data.oxygen_saturation) * 0.5
    heart_risk = data.heart_rate * 0.3
    temp_risk = abs(data.skin_temp - 36.5) * 0.1  # 理想値36.5℃からの逸脱
    activity_risk = data.activity_level * 0.1

    total_score = oxygen_risk + heart_risk + temp_risk + activity_risk

    # 推奨ロジックとリスク判定
    if data.oxygen_saturation < 90:
        recommendation = "🛑 Dangerously low oxygen level. Surface immediately and seek medical attention."
        risk_level = "Critical"
    elif data.heart_rate > 110 and data.oxygen_saturation < 95:
        recommendation = "⚠️ Possible hypoxia. Stop activity and rest."
        risk_level = "High"
    elif data.skin_temp < 32:
        recommendation = "🥶 Risk of hypothermia. Exit water and warm up."
        risk_level = "High"
    elif total_score > 70:
        recommendation = "🚨 High stress detected. Rest immediately."
        risk_level = "High"
    elif total_score > 50:
        recommendation = "⚠️ Moderate stress. Monitor and reduce activity."
        risk_level = "Moderate"
    else:
        recommendation = "✅ Vitals stable. Continue with caution."
        risk_level = "Low"

    return {
        "stressScore": round(total_score, 2),
        "riskLevel": risk_level,
        "oxygenRisk": round(oxygen_risk, 2),
        "heartRisk": round(heart_risk, 2),
        "temperatureRisk": round(temp_risk, 2),
        "activityRisk": round(activity_risk, 2),
        "recommendedProduct": recommendation
    }