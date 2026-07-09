import cv2
import numpy as np


class Dashboard:

    @staticmethod
    def draw(frame, features, analysis, session_time, bad_posture_time, calibration):

        height, width = frame.shape[:2]

        panel_width = 400

        # Create canvas
        canvas = np.zeros((height, width + panel_width, 3), dtype=np.uint8)

        # Copy webcam frame
        canvas[:, :width] = frame

        # Dashboard background
        cv2.rectangle(
            canvas,
            (width, 0),
            (width + panel_width, height),
            (35, 35, 35),
            -1
        )

        # Layout constants
        LEFT = width + 25
        VALUE = width + 230
        RIGHT_EDGE = width + panel_width - 20

        # -------------------------
        # Title
        # -------------------------

        cv2.putText(
            canvas,
            "POSTURESENSE AI",
            (LEFT, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.line(
            canvas,
            (LEFT, 50),
            (RIGHT_EDGE, 50),
            (100, 100, 100),
            1
        )

        # -------------------------
        # Metrics
        # -------------------------

        metrics = [
            ("Neck Angle", f"{features['neck_angle']:.1f} deg"),
            ("Back Angle", f"{features['back_angle']:.1f} deg"),
            ("Shoulder Tilt", f"{features['shoulder_tilt']:.3f}"),
            ("Head Offset", f"{features['head_offset']:.3f}")
        ]

        y = 85

        for label, value in metrics:

            cv2.putText(
                canvas,
                label,
                (LEFT, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (180, 180, 180),
                1
            )

            cv2.putText(
                canvas,
                value,
                (VALUE, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            y += 35

        # Divider
        cv2.line(
            canvas,
            (LEFT, 235),
            (RIGHT_EDGE, 235),
            (100, 100, 100),
            1
        )

        # -------------------------
        # Score
        # -------------------------

        cv2.putText(
            canvas,
            "POSTURE SCORE",
            (LEFT, 265),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (180, 180, 180),
            2
        )

        cv2.putText(
            canvas,
            f"{analysis['score']}/100",
            (LEFT, 305),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            analysis["color"],
            3
        )

        # -------------------------
        # Progress Bar
        # -------------------------

        bar_x = LEFT
        bar_y = 325
        bar_width = 320
        bar_height = 20

        # Background
        cv2.rectangle(
            canvas,
            (bar_x, bar_y),
            (bar_x + bar_width, bar_y + bar_height),
            (70, 70, 70),
            -1
        )

        filled = int(bar_width * analysis["score"] / 100)

        # Filled part
        cv2.rectangle(
            canvas,
            (bar_x, bar_y),
            (bar_x + filled, bar_y + bar_height),
            analysis["color"],
            -1
        )

        # Border
        cv2.rectangle(
            canvas,
            (bar_x, bar_y),
            (bar_x + bar_width, bar_y + bar_height),
            (255, 255, 255),
            2
        )

        # -------------------------
        # Status
        # -------------------------

        cv2.putText(
            canvas,
            "Status",
            (LEFT, 375),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (180, 180, 180),
            1
        )

        cv2.putText(
            canvas,
            analysis["status"],
            (VALUE, 375),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            analysis["color"],
            2
        )

        # -------------------------
        # Session Timer
        # -------------------------

        cv2.putText(
            canvas,
            "Session",
            (LEFT, 410),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (180, 180, 180),
            1
        )

        cv2.putText(
            canvas,
            session_time,
            (VALUE, 410),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # -------------------------
        # Bad Posture Timer
        # -------------------------

        minutes = bad_posture_time // 60
        seconds = bad_posture_time % 60

        bad_time = f"{minutes:02}:{seconds:02}"

        cv2.putText(
            canvas,
            "Bad Time",
            (LEFT, 445),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (180, 180, 180),
            1
        )

        cv2.putText(
            canvas,
            bad_time,
            (VALUE, 445),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

    
        return canvas