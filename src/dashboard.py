import cv2
import numpy as np

# -------------------------
# UI COLORS
# -------------------------

BG = (35, 35, 35)
CARD = (45, 45, 45)

WHITE = (245, 245, 245)
GRAY = (170, 170, 170)
LIGHT_GRAY = (120, 120, 120)

PINK = (180, 105, 255)        # Soft blush pink (BGR)
PINK_LIGHT = (210, 160, 255)

GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 255)
RED = (0, 0, 255)

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
    def rounded_rectangle(img, pt1, pt2, color, radius=20, thickness=2):

        x1, y1 = pt1
        x2, y2 = pt2

        # Straight edges
        cv2.line(img, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
        cv2.line(img, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
        cv2.line(img, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
        cv2.line(img, (x2, y1 + radius), (x2, y2 - radius), color, thickness)

        # Rounded corners
        cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius),
                    180, 0, 90, color, thickness)

        cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius),
                    270, 0, 90, color, thickness)

        cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius),
                    90, 0, 90, color, thickness)

        cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius),
                    0, 0, 90, color, thickness)


    @staticmethod
    def draw(frame, features, analysis, session_time, recommendation, bad_posture_time, summary, page, trend):

        height, width = frame.shape[:2]
        dashboard_height = max(height, 700)
        panel_width = 450

        # Create canvas
        canvas = np.zeros((dashboard_height, width + panel_width, 3),dtype=np.uint8)

        # Copy webcam frame
        canvas[:height, :width] = frame

        # Dashboard background
        cv2.rectangle(
            canvas,
            (width, 0),
            (width + panel_width, dashboard_height),
            (35, 35, 35),
            -1
        )

        Dashboard.rounded_rectangle(
            canvas,
            (width + 8, 8),
            (width + panel_width - 8, dashboard_height - 8),
            (105, 90, 120),
            radius=18,
            thickness=1
        )


        # Layout constants
        LEFT = width + 25
        RIGHT = width + panel_width - 25

        # -------------------------
        # Title
        # -------------------------

        title = "POSTURE SENSE AI"

        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1.15
        thickness = 2

        title_size = cv2.getTextSize(
            title,
            font,
            scale,
            thickness
        )[0]

        title_x = LEFT + ((RIGHT - LEFT) - title_size[0]) // 2

        cv2.putText(
            canvas,
            title,
            (title_x, 48),
            font,
            scale,
            WHITE,
            thickness
        )

        cv2.line(
            canvas,
            (LEFT, 65),
            (RIGHT, 65),
            PINK_LIGHT,
            1
        )

        y = 120

        # -------------------------
        # Split
        # -------------------------

        if page == 0:       # (Existing live dashboard code)
            # -------------------------
            # Metrics
            # -------------------------

            cv2.putText(
                canvas,
                "POSTURE METRICS",
                (LEFT, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                PINK_LIGHT,
                2
            )
            y += 40

            
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
                (120,100,140),
                1
            )

            y += 45

            # -------------------------
            # Score Header
            # -------------------------

            cv2.putText(
                canvas,
                "POSTURE SCORE",
                (LEFT, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                PINK_LIGHT,
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
                (RIGHT-score_size[0], y+5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                PINK_LIGHT,
                5
            )

            cv2.putText(
                canvas,
                score_text,
                (RIGHT-score_size[0], y+5),
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

            y += 60

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

            y += 30

            # =============================
            # Divider
            # =============================

            cv2.line(
                canvas,
                (LEFT, y),
                (RIGHT, y),
                (120,100,140),
                1
            )

            y += 45

            # =============================
            # Recommendation
            # =============================

            cv2.putText(
                canvas,
                "RECOMMENDATION",
                (LEFT, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                PINK_LIGHT,
                2
            )

            y += 40

            tip = recommendation["suggestions"][0]

            lines = Dashboard.wrap_text(
                tip,
                max_chars=30
            )

            for line in lines:

                cv2.putText(
                    canvas,
                    line,
                    (LEFT, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.52,
                    WHITE,
                    1
                )

                y += 26

            

            # =============================
            # Divider
            # =============================

            cv2.line(
                canvas,
                (LEFT, y),
                (RIGHT, y),
                (120,100,140),
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
                0.75,
                PINK_LIGHT,
                2
            )
            y += 35

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

                y += 28


            #divider
            cv2.line(
                canvas,
                (LEFT, y),
                (RIGHT, y),
                (120,100,140),
                1
            )

            y += 35

            # =============================
            # Posture Distribution
            # =============================
            cv2.putText(
                canvas,
                "POSTURE DISTRIBUTION",
                (LEFT, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                PINK_LIGHT,
                2
            )
            y += 35


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
                    0.55,
                    (180,180,180),
                    1
                )

                value = f"{percent}%"

                size = cv2.getTextSize(
                    value,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
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

                y += 26

            # =============================
            # Trend Graph
            # =============================
            cv2.line(
                canvas,
                (LEFT, y),
                (RIGHT, y),
                (120,100,140),
                1
            )

            y += 35

            cv2.putText(
                canvas,
                "POSTURE TREND",
                (LEFT, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                PINK_LIGHT,
                2
            )
            y += 30


            trend.draw(
                canvas,
                LEFT + 25,
                y,
                RIGHT - LEFT - 25,
                120
            )


        # =============================
        # FOOTER
        # =============================

        footer = "[TAB] Analytics" if page == 0 else "[TAB] Live Dashboard"
        cv2.putText(
            canvas,
            "[TAB]",
            (LEFT, dashboard_height - 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            PINK,
            1
        )

        cv2.putText(
            canvas,
            " Switch Dashboard",
            (LEFT + 42, dashboard_height - 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            GRAY,
            1
        )


        return canvas