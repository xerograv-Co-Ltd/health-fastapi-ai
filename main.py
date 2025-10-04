from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models.rule_based_engine import RuleBasedEngine
from storage.csv_logger import append_to_csv_log
from models.predict_engine import PredictEngine

app = FastAPI()

# --- DiveComputerSample構成 ---
class DCTissueSnapshot(BaseModel):
    i: int
    p: float
    pctM: float

class DiveComputerSample(BaseModel):
    id: str
    t: int
    depthM: Optional[float]
    hr: Optional[int]
    tissues: List[DCTissueSnapshot]

class DiveBatchRequest(BaseModel):
    uid: str
    session_id: str
    samples: List[DiveComputerSample]

# --- エンドポイント ---
@app.post("/analyze_batch")
def analyze_batch(batch: DiveBatchRequest):
    engine = RuleBasedEngine()
    results = []

    for sample in batch.samples:
        max_pctM = max((t.pctM for t in sample.tissues), default=0.0)
        result = engine.evaluate(sample.depthM, sample.hr, max_pctM)

        append_to_csv_log({
            "timestamp": datetime.utcnow().isoformat(),
            "heart_rate": sample.hr or 0,
            "oxygen_saturation": None,  # 未取得のため
            "temperature": None,
            "depth": sample.depthM or 0.0,
            "max_percent_m": max_pctM
        }, result)

        results.append({
            "elapsed_sec": sample.t,
            "risk_level": result["riskLevel"],
            "risk_score": result["stressScore"]
        })

    return {
        "uid": batch.uid,
        "session_id": batch.session_id,
        "results": results
    }

@app.post("/predict_batch")
def predict_batch(batch: DiveBatchRequest):
    results = []

    for sample in batch.samples:
        max_pctM = max((t.pctM for t in sample.tissues), default=0.0)

        # ML予測
        pred = predictor.predict(
            heart_rate=sample.hr,
            oxygen_saturation=None,  # 現時点では無し
            temperature=None,
            depth=sample.depthM,
            max_percent_m=max_pctM
        )

        results.append({
            "elapsed_sec": sample.t,
            "predicted_label": pred["label"],
            "confidence": pred["confidence"]
        })

    return {
        "uid": batch.uid,
        "session_id": batch.session_id,
        "results": results
    }
