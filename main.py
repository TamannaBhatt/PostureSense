import cv2
from src.pose_detector import PoseDetector
from src.feature_extractor import FeatureExtractor

# Initialize webcam
cap = cv2.VideoCapture(0)

# Create PoseDetector object
detector = PoseDetector()

while True:

    success, frame = cap.read()

    if not success:
        break

    # Flip the frame for a mirror view
    frame = cv2.flip(frame, 1)

    # Detect pose and get landmarks
    frame, landmarks = detector.detect_pose(frame)

    # If landmarks are detected
    if landmarks:

        mp_pose = detector.mp_pose

        # Extract important landmarks
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Display coordinates on screen
        cv2.putText(
            frame,
            f"Nose: ({nose.x:.2f}, {nose.y:.2f})",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"L Shoulder: ({left_shoulder.x:.2f}, {left_shoulder.y:.2f})",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"R Shoulder: ({right_shoulder.x:.2f}, {right_shoulder.y:.2f})",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        left_ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        left_knee = landmarks[ mp_pose.PoseLandmark.LEFT_KNEE.value ]


        ear = (left_ear.x, left_ear.y)
        shoulder = (left_shoulder.x, left_shoulder.y)
        hip = (left_hip.x, left_hip.y)
        knee = (left_knee.x,left_knee.y)
        left_shoulder_point = (left_shoulder.x, left_shoulder.y)
        right_shoulder_point = (right_shoulder.x, right_shoulder.y)


        neck_angle = FeatureExtractor.calculate_angle( ear, shoulder, hip)
        back_angle = FeatureExtractor.calculate_angle(shoulder, hip, knee)
        shoulder_tilt = FeatureExtractor.calculate_shoulder_tilt(left_shoulder_point,right_shoulder_point)

        cv2.putText(
            frame, f"Neck Angle: {neck_angle:.1f}",(10,120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2
        )

        cv2.putText(
            frame, f"Back Angle: {back_angle:.1f}",(10, 150),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
            (255, 255, 0), 2 ) 

        cv2.putText(
            frame, f"Shoulder Tilt: {shoulder_tilt:.3f}", (10, 180),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
            (255, 0, 255), 2)
        
    # Display the webcam
    cv2.imshow("PostureSense AI", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()