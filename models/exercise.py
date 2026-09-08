class Exercise:
    def __init__(self, exercise_id, exercise_name, course, max_score=20, score=None):
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.course = course
        self.max_score = max_score
        self.score = score