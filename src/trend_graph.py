import cv2
import numpy as np


class TrendGraph:

    def __init__(self, max_points=60):

        self.max_points = max_points
        self.points = []

    def update(self, score):

        self.points.append(int(score))

        if len(self.points) > self.max_points:
            self.points.pop(0)

    def draw(self, canvas, x, y, width, height):

        # Background
        cv2.rectangle(
            canvas,
            (x, y),
            (x + width, y + height),
            (45, 45, 45),
            -1
        )

        # Border
        cv2.rectangle(
            canvas,
            (x, y),
            (x + width, y + height),
            (120, 120, 120),
            1
        )

        # -------------------------
        # Grid + Labels
        # -------------------------

        for i in range(5):

            yy = int(y + i * height / 4)

            cv2.line(
                canvas,
                (x, yy),
                (x + width, yy),
                (70, 70, 70),
                1
            )

            value = str(100 - i * 25)

            cv2.putText(
                canvas,
                value,
                (x - 28, yy + 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (170, 170, 170),
                1
            )

        if len(self.points) < 2:
            return

        pts = []

        for i, score in enumerate(self.points):

            px = int(
                x + i * width / (self.max_points - 1)
            )

            py = int(
                y + height - (score / 100) * height
            )

            pts.append((px, py))

        pts = np.array(pts, np.int32)



        for i in range(1, len(pts)):

            score = self.points[i]

            if score >= 90:
                color = (0,255,0)

            elif score >= 80:
                color = (0,255,255)

            elif score >= 70:
                color = (0,165,255)

            else:
                color = (0,0,255)

            cv2.line(
                canvas,
                tuple(pts[i-1]),
                tuple(pts[i]),
                color,
                2
            )

        latest_score = self.points[-1]

        if latest_score >= 90:
            latest_color = (0,255,0)
        elif latest_score >= 80:
            latest_color = (0,255,255)
        elif latest_score >= 70:
            latest_color = (0,165,255)
        else:
            latest_color = (0,0,255)

        # Outer colored ring
        
        cv2.circle(                                        # Glow
            canvas, tuple(pts[-1]), 9, latest_color, 1
        )

        cv2.circle(                                        # Ring
            canvas, tuple(pts[-1]), 6, latest_color, -1
        )

        cv2.circle(                                        # Center
            canvas, tuple(pts[-1]), 3, (255,255,255), -1
        )

        # Inner white dot
        cv2.circle(
            canvas,
            tuple(pts[-1]),
            3,
            (255,255,255),
            -1
        )