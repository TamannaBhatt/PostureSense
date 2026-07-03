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
    
    @staticmethod
    def calculate_head_offset(ear, shoulder):
        """
        Returns horizontal distance between ear and shoulder.
        Larger value indicates forward head posture.
        """
        return abs(ear[0] - shoulder[0])
    
    @staticmethod
    def extract_features(landmarks, mp_pose):

        left_ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]

        ear = (left_ear.x, left_ear.y)
        shoulder = (left_shoulder.x, left_shoulder.y)
        hip = (left_hip.x, left_hip.y)
        knee = (left_knee.x, left_knee.y)

        left_shoulder_point = (
            left_shoulder.x, left_shoulder.y
        )

        right_shoulder_point = (
            right_shoulder.x, right_shoulder.y
        )

        neck_angle = FeatureExtractor.calculate_angle(
            ear, shoulder, hip
        )

        back_angle = FeatureExtractor.calculate_angle(
            shoulder, hip, knee
        )

        shoulder_tilt = FeatureExtractor.calculate_shoulder_tilt(
            left_shoulder_point, right_shoulder_point
        )

        head_offset = FeatureExtractor.calculate_head_offset(
            ear, shoulder
        )

        return {
            "neck_angle": neck_angle,
            "back_angle": back_angle,
            "shoulder_tilt": shoulder_tilt,
            "head_offset": head_offset
        }