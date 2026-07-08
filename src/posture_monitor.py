import time


class PostureMonitor:

    def __init__(self):
        self.bad_posture_start = None
        self.bad_posture_duration = 0

    def update(self, status):

        if status in ["Fair", "Poor"]:

            if self.bad_posture_start is None:
                self.bad_posture_start = time.time()

            self.bad_posture_duration = int(
                time.time() - self.bad_posture_start
            )

        else:

            self.bad_posture_start = None
            self.bad_posture_duration = 0

        return self.bad_posture_duration