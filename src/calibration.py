import json
import os
import time


class Calibration:

    def __init__(self):

        self.filename = "data/calibration.json"

        self.calibrating = False
        self.completed = False

        self.start_time = None
        self.duration = 5          # seconds

        self.samples = []

        self.reference = {}

    def start(self):

        self.calibrating = True
        self.completed = False

        self.start_time = time.time()

        self.samples = []

    def collect(self, features):

        if not self.calibrating:
            return

        self.samples.append(features.copy())

        elapsed = time.time() - self.start_time

        if elapsed >= self.duration:

            self.finish()

    def finish(self):

        avg = {}

        keys = self.samples[0].keys()

        for key in keys:

            avg[key] = sum(sample[key] for sample in self.samples) / len(self.samples)

        self.reference = avg

        os.makedirs("data", exist_ok=True)

        with open(self.filename, "w") as f:

            json.dump(
                {
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "samples": len(self.samples),
                    "baseline": avg
                },
                f,
                indent=4
            )

        self.calibrating = False
        self.completed = True
        self.completed_time = time.time()

    def remaining_time(self):

        if not self.calibrating:
            return 0

        return max(
            0,
            self.duration - int(time.time() - self.start_time)
        )
    
    def get_baseline(self):

        if not self.reference:
            return None

        if "baseline" in self.reference:
            return self.reference["baseline"]

        return self.reference
    
    def load(self):

        if not os.path.exists(self.filename):
            return

        with open(self.filename, "r") as f:
            self.reference = json.load(f)