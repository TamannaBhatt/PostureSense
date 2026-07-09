class RecommendationEngine:

    @staticmethod
    def generate(features, baseline=None):

        issues = []
        suggestions = []

        neck = features["neck_angle"]
        back = features["back_angle"]
        shoulder = abs(features["shoulder_tilt"])
        head = features["head_offset"]

        # -----------------------------
        # Head Position
        # -----------------------------
        if head > 0.15:
            issues.append("Head leaning forward")
            suggestions.append("Raise monitor to eye level.")

        # -----------------------------
        # Neck
        # -----------------------------
        if neck < 150:
            issues.append("Neck bent forward")
            suggestions.append("Keep your neck upright.")

        # -----------------------------
        # Back
        # -----------------------------
        if back < 175:
            issues.append("Rounded back")
            suggestions.append("Sit back against the chair.")

        # -----------------------------
        # Shoulders
        # -----------------------------
        if shoulder > 0.03:
            issues.append("Uneven shoulders")
            suggestions.append("Relax both shoulders evenly.")

        if not issues:

            issues.append("Excellent posture!")

            suggestions.append(
                "Maintain your current posture."
            )

        return {

            "issues": issues,

            "suggestions": suggestions

        }