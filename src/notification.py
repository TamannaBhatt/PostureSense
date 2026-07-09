import cv2
import time


class Notification:

    def __init__(self):
        self.message = ""
        self.color = (255, 255, 255)
        self.end_time = 0

    def show(self, message, color=(255, 255, 255), duration=2):
        self.message = message
        self.color = color
        self.end_time = time.time() + duration

    def draw(self, frame):

        if time.time() > self.end_time:
            return frame

        h, w = frame.shape[:2]

        lines = self.message.split("\n")

        box_width = 420
        line_height = 30
        padding = 20
        box_height = padding * 2 + line_height * len(lines)

        x = (w - box_width) // 2
        y = 20

        # Background
        cv2.rectangle(
            frame,
            (x, y),
            (x + box_width, y + box_height),
            (40, 40, 40),
            -1
        )

        # Border
        cv2.rectangle(
            frame,
            (x, y),
            (x + box_width, y + box_height),
            self.color,
            2
        )

        current_y = y + 35

        for line in lines:

            text_size = cv2.getTextSize(
                line,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                2
            )[0]

            text_x = x + (box_width - text_size[0]) // 2

            cv2.putText(
                frame,
                line,
                (text_x, current_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            current_y += line_height

        return frame