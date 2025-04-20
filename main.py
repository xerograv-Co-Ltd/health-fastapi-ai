from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    heart_rate: float
    skin_temp: float
    uv_index: float
    pm25: float
    humidity: float

@app.post("/analyze")
def analyze(data: InputData):
    score = data.uv_index * 0.4 + data.pm25 * 0.3 + data.heart_rate * 0.2 + data.skin_temp * 0.1
    if score > 60:
        product = "Take a rest and stop activity"
    elif score > 40:
        product = "Change to safer plan"
    else:
        product = "Keep your safety plan"
    return {"recommendedProduct": product, "stressScore": round(score, 2)}
