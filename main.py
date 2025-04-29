from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    heart_rate: float
    skin_temp: float
    uv_index: float  # ← 使わないが受け取るだけ
    pm25: float      # ← 使わないが受け取るだけ
    humidity: float  # ← 使わないが受け取るだけ
    oxygen_saturation: float
    activity_level: float

@app.post("/analyze")
def analyze(data: InputData):
    score = (
        (100 - data.oxygen_saturation) * 0.5 +
        data.heart_rate * 0.3 +
        data.skin_temp * 0.1 +
        data.activity_level * 0.1
    )
    
    if score > 70:
        product = "Immediate rest and seek help"
    elif score > 50:
        product = "Reduce activity and monitor yourself"
    else:
        product = "Safe to continue activity"
    
    return {"recommendedProduct": product, "stressScore": round(score, 2)}
