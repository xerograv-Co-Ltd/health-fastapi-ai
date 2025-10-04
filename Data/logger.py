import csv
from datetime import datetime

def log_to_csv(data, result, filepath="data/health_log.csv"):
    with open(filepath, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(),
            data.heart_rate,
            data.skin_temp,
            data.oxygen_saturation,
            data.activity_level,
            max_m_percent,
            result["stressScore"],
            result["riskLevel"]
        ])
