import csv
from pathlib import Path

CSV_PATH = Path("data/poc_divelog.csv")
HEADER = [
    "timestamp",
    "heart_rate",
    "oxygen_saturation",
    "temperature",
    "depth",
    "max_percent_m",
    "risk_score",
    "risk_level",
    "label"
]

def append_to_csv_log(sample, result, label=None):
    """DiveSample + 推定結果 + label をCSVに追記"""
    exists = CSV_PATH.exists()
    with open(CSV_PATH, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(HEADER)
        writer.writerow([
            sample["timestamp"],
            sample["heart_rate"],
            sample["oxygen_saturation"] or "",
            sample["temperature"] or "",
            sample["depth"],
            sample["max_percent_m"],
            result["stressScore"],
            result["riskLevel"],
            label or ""
        ])
