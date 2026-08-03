class Submission:
    def __init__(self, submission_id, student, exercise, submission_date, file_path, status):
        self.submission_id = submission_id  
        self.student = student
        self.exercise = exercise
        self.submission_date = submission_date
        self.file_path = file_path
        self.status = status