class PostureAnalyzer:

    @staticmethod
    def analyze(features, baseline=None):

        neck = features["neck_angle"]
        back = features["back_angle"]
        shoulder = abs(features["shoulder_tilt"])
        head = features["head_offset"]

        score = 100

        # -----------------------------
        # Use calibrated baseline if available
        # -----------------------------
        if baseline:

            neck_difference = abs(neck - baseline["neck_angle"])
            back_difference = abs(back - baseline["back_angle"])
            shoulder_difference = abs(
                shoulder - abs(baseline["shoulder_tilt"])
            )
            head_difference = abs(
                head - baseline["head_offset"]
            )

            # Neck
            if neck_difference > 10:
                score -= 20
            elif neck_difference > 5:
                score -= 10

            # Back
            if back_difference > 8:
                score -= 20
            elif back_difference > 4:
                score -= 10

            # Shoulder
            if shoulder_difference > 0.05:
                score -= 15
            elif shoulder_difference > 0.03:
                score -= 5

            # Head
            if head_difference > 0.06:
                score -= 20
            elif head_difference > 0.03:
                score -= 10

        # -----------------------------
        # Fallback to default thresholds
        # -----------------------------
        else:

            # Neck
            if neck < 145:
                score -= 20
            elif neck < 150:
                score -= 10

            # Back
            if back < 170:
                score -= 20
            elif back < 175:
                score -= 10

            # Shoulder
            if shoulder > 0.05:
                score -= 15
            elif shoulder > 0.03:
                score -= 5

            # Head
            if head > 0.18:
                score -= 20
            elif head > 0.15:
                score -= 10

        score = max(score, 0)

        # -----------------------------
        # Final Status
        # -----------------------------
        if score >= 90:
            status = "Excellent"
            color = (0, 255, 0)

        elif score >= 75:
            status = "Good"
            color = (0, 255, 255)

        elif score >= 60:
            status = "Fair"
            color = (0, 165, 255)

        else:
            status = "Poor"
            color = (0, 0, 255)

        return {
            "score": score,
            "status": status,
            "color": color
        }