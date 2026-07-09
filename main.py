import cv2
import time

from src.pose_detector import PoseDetector
from src.feature_extractor import FeatureExtractor
from src.posture_analyzer import PostureAnalyzer
from src.posture_monitor import PostureMonitor
from src.logger import PostureLogger
from src.session_timer import SessionTimer
from src.dashboard import Dashboard
from src.calibration import Calibration
from src.calibration_ui import CalibrationUI
from src.notification import Notification


# -----------------------------
# Initialize Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

# -----------------------------
# Initialize Objects
# -----------------------------
detector = PoseDetector()
monitor = PostureMonitor()
logger = PostureLogger()
session = SessionTimer()
warning_shown = False
calibration = Calibration()
calibration.load()
notification = Notification()

# Show startup message
calibration = Calibration()
calibration.load()
notification = Notification()

# Show startup message
if calibration.reference:
    notification.show(
        "Calibration Loaded\nPress C : Recalibrate\nPress Q : Quit",
        (0,255,0),
        duration=5
    )

else:
    notification.show(
        "Calibration Required\nPress C : Calibrate\nPress Q : Quit",
        (0,255,255),
        duration=5
    )
# -----------------------------
# Main Loop
# -----------------------------
while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame, landmarks = detector.detect_pose(frame)

    if landmarks:

        mp_pose = detector.mp_pose

        # -----------------------------
        # Feature Extraction
        # -----------------------------
        features = FeatureExtractor.extract_features(
            landmarks,
            mp_pose
        )

        # -----------------------------
        # Calibration
        # -----------------------------
        calibration.collect(features)
        baseline = calibration.get_baseline()

        # -----------------------------
        # Posture Analysis
        # -----------------------------
        analysis = PostureAnalyzer.analyze(
            features,
            baseline
        )

        # -----------------------------
        # Monitoring
        # -----------------------------
        bad_posture_time = monitor.update(
            analysis["status"]
        )

        session_time = session.get_time()

        # -----------------------------
        # Dashboard
        # -----------------------------
        frame = Dashboard.draw(
            frame,
            features,
            analysis,
            session_time,
            bad_posture_time,
            calibration
        )

        # -----------------------------
        # Logger
        # -----------------------------
        logger.log(
            features,
            analysis
        )

        # -----------------------------
        # Bad Posture Warning
        # -----------------------------
        if bad_posture_time >= 30 and not warning_shown:
            notification.show(
                "Sit Straight!",
                (0, 0, 255),
                duration=2
            )
            warning_shown = True

        elif bad_posture_time < 30:
            warning_shown = False

    else:
        cv2.putText(
            frame,
            "No Person Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    # =====================================
    # Keyboard Input
    # =====================================

    key = cv2.waitKey(1) & 0xFF

    if key == ord("c"):
        if not calibration.calibrating:
            calibration.start()
            notification.show(
                "Calibration Started",
                (0, 255, 255)
            )

    elif key == ord("q"):
        break

    # =====================================
    # Calibration Overlay
    # =====================================

    frame = CalibrationUI.draw(frame, calibration)

    if calibration.completed:
        notification.show(
            "Calibration Complete",
            (0, 255, 0)
        )
        calibration.completed = False
        
    # -----------------------------
    # Show Frame
    # -----------------------------
    frame = notification.draw(frame)
    cv2.imshow(
        "PostureSense AI",
        frame
    )


# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()