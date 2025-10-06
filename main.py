from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models.rule_based_engine import RuleBasedEngine
from storage.csv_logger import append_to_csv_log
from models.predict_engine import PredictEngine

predictor = PredictEngine()
app = FastAPI()

# --- DiveComputerSample構成 ---
class DCTissueSnapshot(BaseModel):
    i: int
    p: float
    pctM: float

class DiveComputerSample(BaseModel):
    id: Optional[str] = None
    t: int
    depthM: Optional[float] = None
    hr: Optional[int] = None
    tissues: Optional[List[DCTissueSnapshot]] = []

class DiveBatchRequest(BaseModel):
    uid: str
    session_id: str
    samples: List[DiveComputerSample]

# --- /analyze_batch ---
@app.post("/analyze_batch")
def analyze_batch(batch: DiveBatchRequest):
    print("📥 Received analyze_batch request")
    print(f"UID: {batch.uid}, Session: {batch.session_id}, Samples: {len(batch.samples)}")

    try:
        engine = RuleBasedEngine()
        results = []

        for sample in batch.samples:
            max_pctM = max((t.pctM for t in sample.tissues or []), default=0.0)
            result = engine.evaluate(sample.depthM, sample.hr, max_pctM)

            append_to_csv_log({
                "timestamp": datetime.utcnow().isoformat(),
                "heart_rate": sample.hr or 0,
                "oxygen_saturation": None,
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

    except Exception as e:
        return {
            "uid": batch.uid,
            "session_id": batch.session_id,
            "results": [],
            "error": str(e)
        }

# --- /predict_batch ---
@app.post("/predict_batch")
def predict_batch(batch: DiveBatchRequest):
    results = []
    predicted_labels = []

    for sample in batch.samples:
        max_pctM = max((t.pctM for t in sample.tissues or []), default=0.0)

        pred = predictor.predict(
            heart_rate=sample.hr,
            oxygen_saturation=None,
            temperature=None,
            depth=sample.depthM,
            max_percent_m=max_pctM
        )

        predicted_labels.append(pred["label"])

        results.append({
            "elapsed_sec": sample.t,
            "predicted_label": pred["label"],
            "confidence": pred["confidence"]
        })

    # 🔽 全体のリスクレベルを算出
    def compute_overall_risk_label(labels: List[str]) -> str:
        if "high" in labels:
            return "high"
        elif "medium" in labels:
            return "medium"
        else:
            return "low"

    overall_risk_level = compute_overall_risk_label(predicted_labels)

    return {
        "uid": batch.uid,
        "session_id": batch.session_id,
        "results": results,
        "overall_risk_level": overall_risk_level  # ✅ 追加済み
    }
