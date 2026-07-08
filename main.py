import cv2

from src.pose_detector import PoseDetector
from src.feature_extractor import FeatureExtractor
from src.posture_analyzer import PostureAnalyzer
from src.posture_monitor import PostureMonitor
from src.logger import PostureLogger
from src.session_timer import SessionTimer
from src.dashboard import Dashboard

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize objects
detector = PoseDetector()
monitor = PostureMonitor()
logger = PostureLogger()
session = SessionTimer()

while True:

    success, frame = cap.read()

    if not success:
        break

    # Mirror the webcam
    frame = cv2.flip(frame, 1)

    # Detect pose
    frame, landmarks = detector.detect_pose(frame)

    if landmarks:

        mp_pose = detector.mp_pose

        # Landmarks (only used for debugging)
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # -------------------------------
        # Feature Extraction
        # -------------------------------
        features = FeatureExtractor.extract_features(
            landmarks,
            mp_pose
        )

        # -------------------------------
        # Posture Analysis
        # -------------------------------
        analysis = PostureAnalyzer.analyze(features)

        # -------------------------------
        # Monitor
        # -------------------------------
        bad_posture_time = monitor.update(
            analysis["status"]
        )

        # -------------------------------
        # Session Timer
        # -------------------------------
        session_time = session.get_time()

        # -------------------------------
        # Dashboard
        # -------------------------------
        frame = Dashboard.draw(
            frame,
            features,
            analysis,
            session_time,
            bad_posture_time
        )

        # -------------------------------
        # CSV Logging
        # -------------------------------
        logger.log(
            features,
            analysis
        )

        # -------------------------------
        # Warning Banner
        # -------------------------------
        if bad_posture_time >= 30:

            cv2.rectangle(
                frame,
                (120, 10),
                (560, 70),
                (0, 0, 255),
                -1
            )

            cv2.putText(
                frame,
                "WARNING: SIT STRAIGHT!",
                (140, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2
            )

    # Display webcam
    cv2.imshow("PostureSense AI", frame)

    # Quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()