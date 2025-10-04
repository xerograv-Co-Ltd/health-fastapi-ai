class RuleBasedEngine:
    def evaluate(self, depth: float | None, heart_rate: int | None, max_pctM: float | None):
        hr = heart_rate or 0
        d = depth or 0.0
        m = max_pctM or 0.0

        score = hr * 0.3 + m * 0.5
        if d > 30: score += 20

        if m > 120 or hr > 130:
            level = "Critical"
        elif m > 100 or hr > 110:
            level = "High"
        elif score > 60:
            level = "Moderate"
        else:
            level = "Low"

        return {
            "stressScore": round(score, 2),
            "riskLevel": level
        }