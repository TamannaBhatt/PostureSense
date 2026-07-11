class Analytics:

    def __init__(self):

        self.total_score = 0
        self.total_frames = 0

        self.best_score = 0
        self.worst_score = 100

        self.status_counts = {
            "Excellent": 0,
            "Good": 0,
            "Fair": 0,
            "Poor": 0
        }

    def update(self, score, status):

        self.total_score += score
        self.total_frames += 1

        self.best_score = max(self.best_score, score)
        self.worst_score = min(self.worst_score, score)

        if status in self.status_counts:
            self.status_counts[status] += 1

    def average_score(self):

        if self.total_frames == 0:
            return 0

        return round(
            self.total_score / self.total_frames,
            1
        )
    
    def status_percentages(self):

        if self.total_frames == 0:

            return {
                status: 0
                for status in self.status_counts
            }

        percentages = {}

        for status, count in self.status_counts.items():

            percentages[status] = round(
                count * 100 / self.total_frames,
                1
            )

        return percentages
    
    def session_grade(self):

        avg = self.average_score()

        if avg >= 90:
            return "A"

        elif avg >= 80:
            return "B"

        elif avg >= 70:
            return "C"

        elif avg >= 60:
            return "D"

        return "F"
    
    def summary(self):

        return {

            "average": self.average_score(),

            "best": self.best_score,

            "worst": self.worst_score,

            "grade": self.session_grade(),

            "percentages": self.status_percentages()

        }