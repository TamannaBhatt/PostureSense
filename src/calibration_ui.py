import cv2


class CalibrationUI:

    @staticmethod
    def draw(frame, calibration):

        if not calibration.calibrating:
            return frame

        h, w = frame.shape[:2]

        box_w = 380
        box_h = 170

        x = (w - box_w) // 2
        y = (h - box_h) // 2

        # Background
        cv2.rectangle(
            frame,
            (x, y),
            (x + box_w, y + box_h),
            (40, 40, 40),
            -1
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + box_w, y + box_h),
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            "CALIBRATING",
            (x + 70, y + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0,255,255),
            2
        )

        cv2.putText(
            frame,
            "Stand Naturally",
            (x + 75, y + 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        progress = (
            (calibration.duration - calibration.remaining_time())
            / calibration.duration
        )

        bar_width = 250
        filled = int(bar_width * progress)

        cv2.rectangle(
            frame,
            (x + 60, y + 105),
            (x + 60 + bar_width, y + 125),
            (70,70,70),
            -1
        )

        cv2.rectangle(
            frame,
            (x + 60, y + 105),
            (x + 60 + filled, y + 125),
            (0,255,0),
            -1
        )

        cv2.rectangle(
            frame,
            (x + 60, y + 105),
            (x + 60 + bar_width, y + 125),
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Samples : {len(calibration.samples)}",
            (x + 80, y + 155),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,255),
            2
        )

        return frame