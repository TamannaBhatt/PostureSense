import csv
import os
import time
from datetime import datetime


class PostureLogger:

    def __init__(self):

        self.filename = "data/posture_logs.csv"
        self.last_log_time = 0

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.filename):

            with open(self.filename, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Timestamp",
                    "Neck Angle",
                    "Back Angle",
                    "Shoulder Tilt",
                    "Head Offset",
                    "Score",
                    "Status"
                ])

    def log(self, features, analysis):

        current_time = time.time()

        if current_time - self.last_log_time < 1:
            return

        self.last_log_time = current_time

        with open(self.filename, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                round(features["neck_angle"],2),
                round(features["back_angle"],2),
                round(features["shoulder_tilt"],4),
                round(features["head_offset"],4),
                analysis["score"],
                analysis["status"]
            ])