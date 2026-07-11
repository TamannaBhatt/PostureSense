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
from src.smoother import FeatureSmoother
from src.recommendation import RecommendationEngine
from src.analytics import Analytics
from src.report_generator import ReportGenerator
from src.screenshot import Screenshot
from src.trend_graph import TrendGraph


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

calibration = Calibration()
calibration.load()

notification = Notification()
smoother = FeatureSmoother()
analytics = Analytics()
trend = TrendGraph()

dashboard_page = 0
last_issue = None

# Show startup message
if calibration.reference:
    notification.show(
        "READY\nPress C : Recalibrate\nR : Save Report\nS : Screenshot\nPress Q : Quit",
        (0,255,0),
        duration=5
    )

else:
    notification.show(
        "CALIBRATION REQUIRED\nPress C : Calibrate\nR : Save Report\nS : Screenshot\nPress Q : Quit",
        (0,255,255),
        duration=5
    )
# -----------------------------
# Main Loop
# -----------------------------
summary = analytics.summary()
session_time = "00:00:00"

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
        features = smoother.smooth(features)
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

        analytics.update(
            analysis["score"],
            analysis["status"]
        )

        trend.update(analysis["score"])

        recommendation = RecommendationEngine.generate(
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

        summary = analytics.summary()

        # -----------------------------
        # Dashboard
        # -----------------------------
        frame = Dashboard.draw(
            frame,
            features,
            analysis,
            session_time,
            recommendation,
            bad_posture_time,
            summary,
            dashboard_page,
            trend
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

        if bad_posture_time >= 30:

            issue = recommendation["issues"][0]
            tip = recommendation["suggestions"][0]

            if issue == "Excellent posture!":
                last_issue = None

            else:
                # Notification color based on posture score
                score = analysis["score"]

                if score >= 70:
                    color = (0, 165, 255)      # Orange
                else:
                    color = (0, 0, 255)        # Red

                # Show notification only when issue changes
                if issue != last_issue:

                    notification.show(
                        f"POSTURE ALERT\n{issue}\n{tip}",
                        color,
                        duration=3
                    )

                    last_issue = issue

        else:
            last_issue = None

    else:
        last_issue = None
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
    if key == 9:      # TAB key
        dashboard_page = 1 - dashboard_page

    if key == ord("c"):
        if not calibration.calibrating:
            calibration.start()
            notification.show(
                "Calibration Started",
                (0, 255, 255)
            )

    elif key == ord("r"):
        filename = ReportGenerator.generate(
            summary,
            session_time
        )
        notification.show(
            "Session Report Saved",
            (0, 255, 0),
            duration=2
        )
        print(f"Report saved: {filename}")

    elif key == ord("s"):

        filename = Screenshot.save(frame)

        notification.show(
            "Screenshot Saved",
            (0, 255, 0),
            duration=2
        )

        print(f"Screenshot saved: {filename}")

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