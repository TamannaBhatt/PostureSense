from pathlib import Path
from datetime import datetime
import cv2


class Screenshot:

    @staticmethod
    def save(frame):

        folder = Path("screenshots")
        folder.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = folder / f"Screenshot_{timestamp}.png"

        # Copy frame so original window isn't modified
        image = frame.copy()

        h, w = image.shape[:2]

        watermark = "Captured by PostureSense AI"
        date = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")

        # Dark background strip
        cv2.rectangle(
            image,
            (0, h - 35),
            (w, h),
            (30, 30, 30),
            -1
        )

        # Watermark (left)
        cv2.putText(
            image,
            watermark,
            (15, h - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        # Timestamp (right)
        text_size = cv2.getTextSize(
            date,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            1
        )[0]

        cv2.putText(
            image,
            date,
            (w - text_size[0] - 15, h - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (180, 180, 180),
            1,
            cv2.LINE_AA
        )

        cv2.imwrite(str(filename), image)

        return str(filename)