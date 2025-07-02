class LearningModule:
    def __init__(self):
        self.data = {}
    def observe(self, user, result):
        self.data.setdefault(user, []).append(result)
    def detect_pattern(self, user):
        return self.data.get(user, [])