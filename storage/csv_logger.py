# storage/csv_logger.py
import csv
from pathlib import Path

CSV_PATH = Path("poc_divelog.csv")
HEADER = [
    "timestamp",
    "heart_rate",
    "oxygen_saturation",
    "temperature",
    "depth",
    "max_percent_m",
    "risk_level",
    "reason",
    "label"  # ← 教師データ用のラベル列
]

def append_to_csv_log(sample, risk_level, reason, label=None):
    """DiveSample + 推定結果 + (optional)label をCSVに追記"""
    exists = CSV_PATH.exists()

    with open(CSV_PATH, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(HEADER)
        writer.writerow([
            sample.timestamp,
            sample.heart_rate,
            sample.oxygen_saturation,
            sample.temperature,
            sample.depth,
            sample.max_percent_m,
            risk_level,
            reason,
            label or ""  # 手動ラベル付け前は空
        ])
