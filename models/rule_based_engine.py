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

    def evaluate_mission(
        self,
        depth_m: float,
        heart_rate: int,
        oxygen_saturation: float,
        max_pct_m: float,
        dive_time_sec: int = 0
    ) -> dict:
        # --- Depth risk (0-100) ---
        if depth_m <= 0:
            depth_risk = 0.0
        elif depth_m <= 20:
            depth_risk = 0.0
        elif depth_m <= 30:
            depth_risk = 20.0
        elif depth_m <= 40:
            depth_risk = 45.0
        else:
            depth_risk = 70.0

        # --- HR risk — diving context (higher baseline is normal) ---
        if heart_rate <= 0:
            hr_risk = 0.0
        elif heart_rate < 50:
            hr_risk = 60.0
        elif heart_rate <= 90:
            hr_risk = 0.0
        elif heart_rate <= 120:
            hr_risk = 30.0 + (heart_rate - 90) * 1.5
        else:
            hr_risk = 90.0

        # --- SpO2 risk (tighter thresholds underwater) ---
        if oxygen_saturation <= 0:
            spo2_risk = 0.0
        elif oxygen_saturation >= 97:
            spo2_risk = 0.0
        elif oxygen_saturation >= 95:
            spo2_risk = 25.0
        elif oxygen_saturation >= 92:
            spo2_risk = 70.0
        else:
            spo2_risk = 100.0

        # --- %M tissue saturation risk ---
        if max_pct_m <= 0:
            pctm_risk = 0.0
        elif max_pct_m < 80:
            pctm_risk = 0.0
        elif max_pct_m < 100:
            pctm_risk = 30.0 + (max_pct_m - 80) * 2.0
        elif max_pct_m < 120:
            pctm_risk = 70.0 + (max_pct_m - 100) * 1.5
        else:
            pctm_risk = 100.0

        # --- Weighted stress ---
        stress = (
            depth_risk * 0.20
            + hr_risk * 0.25
            + spo2_risk * 0.35
            + pctm_risk * 0.20
        )
        stress = min(100.0, stress)

        # --- Risk level ---
        if stress < 25:
            level = "Low"
        elif stress < 50:
            level = "Moderate"
        elif stress < 75:
            level = "High"
        else:
            level = "Critical"

        # --- SOS trigger ---
        sos_trigger = (
            (oxygen_saturation > 0 and oxygen_saturation < 90)
            or (heart_rate > 0 and (heart_rate > 140 or heart_rate < 35))
            or max_pct_m > 120
            or depth_m > 60
        )

        # --- Tips ---
        tips = []
        if depth_risk > 40:
            tips.append("深度が深い。浮上速度を守ってください")
        if hr_risk > 30:
            tips.append("心拍数異常。活動量を下げ観察を")
        if spo2_risk > 25:
            tips.append("SpO₂低下。即時浮上を検討してください")
        if pctm_risk > 30:
            tips.append("窒素飽和度上昇。NDL残量を確認してください")
        if not tips:
            tips.append("バイタル良好。安全なダイビングを継続")

        return {
            "stressScore": round(stress, 2),
            "riskLevel": level,
            "perVital": {
                "depthRisk": round(depth_risk, 2),
                "hrRisk": round(hr_risk, 2),
                "spo2Risk": round(spo2_risk, 2),
                "pctMRisk": round(pctm_risk, 2)
            },
            "sosTrigger": sos_trigger,
            "tips": tips
        }

    def evaluate_recovery(
        self,
        dive_duration_sec: int,
        max_depth_m: float,
        max_pct_m: float,
        post_hr: int,
        post_spo2: float,
        surface_interval_planned_min: int = 60
    ) -> dict:
        # --- Deco load risk (0-100) ---
        if max_pct_m < 80:
            deco_risk = 0.0
        elif max_pct_m < 100:
            deco_risk = 20.0 + (max_pct_m - 80) * 1.5
        elif max_pct_m < 120:
            deco_risk = 50.0 + (max_pct_m - 100) * 1.5
        else:
            deco_risk = 80.0

        # --- Depth risk ---
        if max_depth_m <= 20:
            depth_risk = 0.0
        elif max_depth_m <= 30:
            depth_risk = 15.0
        elif max_depth_m <= 40:
            depth_risk = 30.0
        else:
            depth_risk = 50.0

        # --- Duration risk ---
        dive_duration_min = dive_duration_sec / 60
        if dive_duration_min < 30:
            duration_risk = 0.0
        elif dive_duration_min < 60:
            duration_risk = 10.0
        else:
            duration_risk = 25.0

        # --- Post-HR risk ---
        if post_hr <= 0:
            hr_risk = 0.0
        elif post_hr <= 80:
            hr_risk = 0.0
        elif post_hr <= 100:
            hr_risk = 20.0 + (post_hr - 80) * 1.0
        else:
            hr_risk = 40.0

        # --- Post-SpO2 risk ---
        if post_spo2 <= 0:
            spo2_risk = 0.0
        elif post_spo2 >= 97:
            spo2_risk = 0.0
        elif post_spo2 >= 95:
            spo2_risk = 15.0
        elif post_spo2 >= 92:
            spo2_risk = 50.0
        else:
            spo2_risk = 80.0

        # --- Weighted recovery stress ---
        stress = (
            deco_risk * 0.35
            + depth_risk * 0.20
            + duration_risk * 0.10
            + hr_risk * 0.20
            + spo2_risk * 0.15
        )
        stress = min(100.0, stress)
        recovery_score = max(0.0, 100.0 - stress)

        # --- Deco risk summary ---
        if max_pct_m > 120:
            deco_risk_summary = "デコ停止義務あり。緊急医療確認を推奨"
        elif max_pct_m > 100:
            deco_risk_summary = "組織飽和度高。安静と水分補給を継続"
        elif max_pct_m > 80:
            deco_risk_summary = "軽度の窒素残留。休息推奨"
        else:
            deco_risk_summary = "窒素残留は正常範囲"

        # --- Minimum surface interval (hours) ---
        base_interval_h = 1.0
        if max_depth_m > 20:
            base_interval_h += (max_depth_m - 20) / 10 * 0.5
        if max_pct_m > 100:
            base_interval_h += 1.0
        if dive_duration_min > 60:
            base_interval_h += 0.5
        base_interval_h = min(base_interval_h, 24.0)

        # --- Recovery tips ---
        tips = []
        if spo2_risk > 15:
            tips.append("血中酸素が低い。深呼吸と医療確認を")
        if hr_risk > 20:
            tips.append("心拍数が高い。安静にしてください")
        if max_pct_m > 100:
            tips.append("窒素飽和が高かった。次ダイブは余裕を持って")
        if max_depth_m > 30:
            tips.append("深いダイブ後。十分な水分補給と休息を")
        if surface_interval_planned_min < int(base_interval_h * 60):
            tips.append(f"計画インターバルが短すぎます。推奨: {base_interval_h:.1f}時間以上")
        if not tips:
            tips.append("回復状態良好。次ダイブへの準備ができています")

        return {
            "recoveryScore": round(recovery_score, 2),
            "decoRiskSummary": deco_risk_summary,
            "nextDiveMinIntervalH": round(base_interval_h, 1),
            "stressScore": round(stress, 2),
            "recoveryTips": tips
        }
