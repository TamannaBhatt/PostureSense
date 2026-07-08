import cv2
from src.pose_detector import PoseDetector
from src.feature_extractor import FeatureExtractor
from src.posture_analyzer import PostureAnalyzer
from src.posture_monitor import PostureMonitor

# Initialize webcam
cap = cv2.VideoCapture(0)

# Create PoseDetector object
detector = PoseDetector()
monitor = PostureMonitor()

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

        # Get all posture features
        features = FeatureExtractor.extract_features(
            landmarks,
            mp_pose
        )


        analysis = PostureAnalyzer.analyze(features)
        bad_posture_time = monitor.update(
            analysis["status"]
        )

        cv2.putText(
            frame, f"Neck Angle: {features['neck_angle']:.1f}",(10,120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2
        )

        cv2.putText(
            frame, f"Back Angle: {features['back_angle']:.1f}",(10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2 
        ) 

        cv2.putText(
            frame, f"Shoulder Tilt: {features['shoulder_tilt']:.3f}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2
        )

        cv2.putText(
            frame, f"Head Offset: {features['head_offset']:.3f}", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2
        )

        cv2.putText(
            frame, f"Posture Score: {analysis['score']}", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, analysis["color"], 2
        )

        cv2.putText(
            frame, f"Status: {analysis['status']}",(10, 270),cv2.FONT_HERSHEY_SIMPLEX, 0.7, analysis["color"], 2
        )

        cv2.putText(
            frame, f"Bad Posture: {bad_posture_time}s", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0, 0, 255),2
        )
        
        if bad_posture_time >= 30:
            cv2.putText(
                frame,
                "WARNING: SIT STRAIGHT!",
                (220,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                3
            )

    # Display the webcam
    cv2.imshow("PostureSense AI", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()