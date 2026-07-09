import cv2
import numpy as np


class Dashboard:

    @staticmethod
    def wrap_text(text, max_chars=32):

        words = text.split()

        lines = []
        line = ""

        for word in words:

            if len(line + word) <= max_chars:
                line += word + " "
            else:
                lines.append(line.strip())
                line = word + " "

        if line:
            lines.append(line.strip())

        return lines

    @staticmethod
    def draw(frame, features, analysis, session_time, recommendation, bad_posture_time):

        height, width = frame.shape[:2]

        panel_width = 450

        # Create canvas
        canvas = np.zeros((height, width + panel_width, 3),dtype=np.uint8)

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
        RIGHT = width + panel_width - 25

        # -------------------------
        # Title
        # -------------------------

        cv2.putText(
            canvas,
            "POSTURESENSE AI",
            (LEFT, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            (255, 255, 255),
            2
        )

        cv2.line(
            canvas,
            (LEFT, 55),
            (RIGHT, 55),
            (100, 100, 100),
            1
        )

        y = 90

        # -------------------------
        # Metrics
        # -------------------------

        metrics = [
            ("Neck Angle", f"{features['neck_angle']:.1f} deg"),
            ("Back Angle", f"{features['back_angle']:.1f} deg"),
            ("Shoulder Tilt", f"{abs(features['shoulder_tilt']):.3f}"),
            ("Head Offset", f"{features['head_offset']:.3f}")
        ]

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

            value_size = cv2.getTextSize(
                value,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                2
            )[0]

            cv2.putText(
                canvas,
                value,
                (RIGHT - value_size[0], y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            y += 26

        # Divider
        y += 4

        cv2.line(
            canvas,
            (LEFT, y),
            (RIGHT, y),
            (90,90,90),
            1
        )

        y += 20

        # -------------------------
        # Score Header
        # -------------------------

        cv2.putText(
            canvas,
            "POSTURE SCORE",
            (LEFT, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (180,180,180),
            2
        )

        score_text = f"{analysis['score']}/100"

        score_size = cv2.getTextSize(
            score_text,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            2
        )[0]

        cv2.putText(
            canvas,
            score_text,
            (RIGHT - score_size[0], y+5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            analysis["color"],
            2
        )

        y += 25

        # -------------------------
        # Progress Bar
        # -------------------------

        bar_x = LEFT
        bar_y = y

        bar_width = RIGHT - LEFT
        bar_height = 18

        cv2.rectangle(
            canvas,
            (bar_x, bar_y),
            (bar_x + bar_width, bar_y + bar_height),
            (70,70,70),
            -1
        )

        filled = int(bar_width * analysis["score"] / 100)

        cv2.rectangle(
            canvas,
            (bar_x, bar_y),
            (bar_x + filled, bar_y + bar_height),
            analysis["color"],
            -1
        )

        cv2.rectangle(
            canvas,
            (bar_x, bar_y),
            (bar_x + bar_width, bar_y + bar_height),
            (255,255,255),
            2
        )

        y += 45

        # =============================
        # Status
        # =============================

        cv2.putText(
            canvas,
            "Status",
            (LEFT, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (180, 180, 180),
            1
        )

        status = analysis["status"]

        status_size = cv2.getTextSize(
            status,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            2
        )[0]

        cv2.putText(
            canvas,
            status,
            (RIGHT - status_size[0], y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            analysis["color"],
            2
        )

        y += 32

        # =============================
        # Session
        # =============================

        cv2.putText(
            canvas,
            "Session",
            (LEFT, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (180,180,180),
            1
        )

        session_size = cv2.getTextSize(
            session_time,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            2
        )[0]

        cv2.putText(
            canvas,
            session_time,
            (RIGHT - session_size[0], y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255,255,255),
            2
        )

        y += 30


        # =============================
        # Bad Time
        # =============================

        minutes = bad_posture_time // 60
        seconds = bad_posture_time % 60
        bad_time = f"{minutes:02}:{seconds:02}"

        cv2.putText(
            canvas,
            "Bad Time",
            (LEFT, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (180,180,180),
            1
        )

        bad_size = cv2.getTextSize(
            bad_time,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            2
        )[0]

        cv2.putText(
            canvas,
            bad_time,
            (RIGHT - bad_size[0], y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255,255,255),
            2
        )

        y += 30

        # =============================
        # Divider
        # =============================

        cv2.line(
            canvas,
            (LEFT, y),
            (RIGHT, y),
            (90, 90, 90),
            1
        )

        y += 22

        # =============================
        # Recommendation
        # =============================

        cv2.putText(
            canvas,
            "RECOMMENDATION",
            (LEFT , y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (180, 180, 180),
            2
        )

        y += 25

        # Issue

        issue = recommendation["issues"][0] if recommendation["issues"] else "None"

        issue_lines = Dashboard.wrap_text(
            "Issue: " + issue
        )

        for line in issue_lines:

            cv2.putText(
                canvas,
                line,
                (LEFT + 10, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0,180,255),
                2
            )

            y += 18

        # Tip
        tip = recommendation["suggestions"][0] if recommendation["suggestions"] else "-"

        tip_lines = Dashboard.wrap_text(
            "Tip: " + tip
        )

        for line in tip_lines:

            cv2.putText(
                canvas,
                line,
                (LEFT +10, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0,255,0),
                2
            )

            y += 16

        return canvas