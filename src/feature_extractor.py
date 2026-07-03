import math

class FeatureExtractor:

    @staticmethod
    def calculate_angle(a, b, c):
        """
        Calculates angle ABC in degrees.
        """

        angle = math.degrees(
            math.atan2(c[1] - b[1], c[0] - b[0])
            -
            math.atan2(a[1] - b[1], a[0] - b[0])
        )

        angle = abs(angle)

        if angle > 180:
            angle = 360 - angle

        return angle
    
    @staticmethod
    def calculate_shoulder_tilt(left_shoulder, right_shoulder):
        """
        Returns the vertical difference between shoulders.
        Positive -> Left shoulder is lower.
        Negative -> Right shoulder is lower.
        """

        return left_shoulder[1] - right_shoulder[1]