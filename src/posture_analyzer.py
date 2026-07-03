class PostureAnalyzer:

    @staticmethod
    def analyze(features):

        neck = features["neck_angle"]
        back = features["back_angle"]
        shoulder = abs(features["shoulder_tilt"])
        head = features["head_offset"]

        score = 100

        # Neck Angle
        if neck < 145:
            score -= 20
        elif neck < 150:
            score -= 10

        # Back Angle
        if back < 170:
            score -= 20
        elif back < 175:
            score -= 10

        # Shoulder Tilt
        if shoulder > 0.05:
            score -= 15
        elif shoulder > 0.03:
            score -= 5

        # Head Offset
        if head > 0.18:
            score -= 20
        elif head > 0.15:
            score -= 10

        score = max(score, 0)

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