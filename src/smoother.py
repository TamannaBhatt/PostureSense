class FeatureSmoother:

    def __init__(self, alpha=0.2):

        self.alpha = alpha
        self.values = {}

    def smooth(self, features):

        smoothed = {}

        for key, value in features.items():

            if key not in self.values:

                self.values[key] = value

            else:

                self.values[key] = (
                    self.alpha * value
                    +
                    (1 - self.alpha) * self.values[key]
                )

            smoothed[key] = self.values[key]

        return smoothed