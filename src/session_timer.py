import time


class SessionTimer:

    def __init__(self):
        self.start_time = time.time()

    def get_time(self):

        elapsed = int(time.time() - self.start_time)

        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"