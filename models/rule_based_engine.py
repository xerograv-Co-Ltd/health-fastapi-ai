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

    def evaluate_readiness(
        self,
        heart_rate: int,
        oxygen_saturation: float,
        skin_temp: float,
        activity_level: float
    ) -> dict:
        # --- HR risk (0-100) ---
        if heart_rate <= 0:
            hr_risk = 0.0
        elif heart_rate < 50:
            hr_risk = 50.0
        elif heart_rate <= 80:
            hr_risk = 0.0
        elif heart_rate <= 100:
            hr_risk = 20.0 + (heart_rate - 80) * 2.0
        else:
            hr_risk = 80.0

        # --- SpO2 risk (0-100) ---
        if oxygen_saturation <= 0:
            spo2_risk = 0.0
        elif oxygen_saturation >= 97:
            spo2_risk = 0.0
        elif oxygen_saturation >= 95:
            spo2_risk = 20.0
        elif oxygen_saturation >= 92:
            spo2_risk = 60.0
        else:
            spo2_risk = 100.0

        # --- Skin temperature risk (0-100) ---
        if skin_temp <= 0:
            temp_risk = 0.0
        elif skin_temp < 31:
            temp_risk = 60.0
        elif skin_temp < 33:
            temp_risk = 30.0
        elif skin_temp <= 36:
            temp_risk = 0.0
        else:
            temp_risk = 40.0

        # --- Activity risk (0-100) ---
        if activity_level < 200:
            activity_risk = 0.0
        elif activity_level < 500:
            activity_risk = 15.0
        else:
            activity_risk = 30.0

        # --- Weighted stress score ---
        stress = (
            hr_risk * 0.40
            + spo2_risk * 0.40
            + temp_risk * 0.15
            + activity_risk * 0.05
        )
        stress = min(100.0, stress)
        readiness_score = max(0.0, 100.0 - stress)

        # --- Risk level ---
        if stress < 20:
            level = "Low"
        elif stress < 40:
            level = "Moderate"
        elif stress < 60:
            level = "High"
        else:
            level = "Critical"

        # --- Go / No-Go ---
        if readiness_score >= 75:
            go_no_go = "go"
        elif readiness_score >= 55:
            go_no_go = "caution"
        else:
            go_no_go = "no_go"

        # --- Tips ---
        tips = []
        if hr_risk > 40:
            tips.append("心拍数が高め。十分な休息を取ってください")
        if spo2_risk > 20:
            tips.append("血中酸素が低め。深呼吸と水分補給を")
        if temp_risk > 30:
            tips.append("体温異常。適切な服装と体温管理を")
        if activity_risk > 15:
            tips.append("活動量が多い。十分な休息後にダイビングを")
        if not tips:
            tips.append("コンディション良好。安全なダイビングを！")

        # --- Recommended product ---
        if temp_risk > 30 and skin_temp > 0 and skin_temp < 33:
            recommended_product = "5mm ウェットスーツ / ドライスーツ"
        else:
            recommended_product = "装備は標準で OK"

        return {
            "stressScore": round(stress, 2),
            "riskLevel": level,
            "oxygenRisk": round(spo2_risk, 2),
            "heartRisk": round(hr_risk, 2),
            "temperatureRisk": round(temp_risk, 2),
            "activityRisk": round(activity_risk, 2),
            "recommendedProduct": recommended_product,
            "readinessScore": round(readiness_score, 2),
            "goNoGo": go_no_go,
            "tips": tips
        }
