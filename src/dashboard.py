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
    def draw(frame, features, analysis, session_time, recommendation, bad_posture_time, summary, page):

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
        # Split
        # -------------------------

        if page == 0:       # (Existing live dashboard code)
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

            y += 30

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
            
        else:                                     # (Analytics dashboard)
            # =============================
            # SESSION SUMMARY
            # =============================

            cv2.putText(
                canvas,
                "SESSION ANALYTICS",
                (LEFT, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.70,
                (180,180,180),
                2
            )

            y += 40

            items = [
                ("Session", session_time),

                ("Average Score", f"{summary['average']:.1f}"),

                ("Best Score", str(summary["best"])),

                ("Worst Score", str(summary["worst"])),

                ("Grade", summary["grade"])

            ]

            for label, value in items:

                cv2.putText(
                    canvas,
                    label,
                    (LEFT, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (180,180,180),
                    1
                )

                value_size = cv2.getTextSize(
                    value,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    2
                )[0]

                color = (255,255,255)

                if label == "Grade":

                    if value == "A":
                        color = (0,255,0)

                    elif value == "B":
                        color = (0,255,255)

                    elif value == "C":
                        color = (0,165,255)

                    else:
                        color = (0,0,255)

                cv2.putText(
                    canvas,
                    value,
                    (RIGHT - value_size[0], y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    color,
                    2
                )

                y += 35


            #divider
            cv2.line(
                canvas,
                (LEFT, y),
                (RIGHT, y),
                (90,90,90),
                1
            )

            y += 30

            #percentage
            percentages = summary["percentages"]

            rows = [

                ("Excellent", percentages["Excellent"], (0,255,0)),

                ("Good", percentages["Good"], (0,255,255)),

                ("Fair", percentages["Fair"], (0,165,255)),

                ("Poor", percentages["Poor"], (0,0,255))

            ]

            for label, percent, color in rows:

                cv2.putText(
                    canvas,
                    label,
                    (LEFT, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.52,
                    (180,180,180),
                    1
                )

                value = f"{percent}%"

                size = cv2.getTextSize(
                    value,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.52,
                    2
                )[0]

                cv2.putText(
                    canvas,
                    value,
                    (RIGHT - size[0], y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.52,
                    color,
                    2
                )

                y += 30



            cv2.line(
                canvas,
                (LEFT, height - 45),
                (RIGHT, height - 45),
                (90,90,90),
                1
            )

        # =============================
        # FOOTER
        # =============================

        footer = "[TAB] Analytics" if page == 0 else "[TAB] Live Dashboard"
        cv2.putText(
            canvas,
            footer,
            (LEFT, height - 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (150,150,150),
            1
        )


        return canvas