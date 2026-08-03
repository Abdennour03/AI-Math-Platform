class SubmissionRepo:
    def __init__(self):
        self.submissions = []

    def add_submission(self, submission):
        self.submissions.append(submission)

    def get_submission(self, submission_id):
        for submission in self.submissions:
            if submission.submission_id == submission_id:
                return submission
        return None 


    def get_all_submissions(self):
        return self.submissions

    def update_submission(self, submission_id, **kwargs):
        for submission in self.submissions:
            if submission.submission_id == submission_id:
                for key, value in kwargs.items():
                    if hasattr(submission, key):
                        setattr(submission, key, value)
                return True 
        return False

    def delete_submission(self, submission_id):
        for index, submission in enumerate(self.submissions):
            if submission.submission_id == submission_id:
                del self.submissions[index]
                return True
        return False

    def search_submission_by_student(self, student_id):
        result_submissions = []
        for submission in self.submissions:
            if submission.student.student_id == student_id:
                result_submissions.append(submission)
        return result_submissions
    
    def search_submission_by_exercise(self, exercise_id):
        result_submissions = []
        for submission in self.submissions:
            if submission.exercise.exercise_id == exercise_id:
                result_submissions.append(submission)
        return result_submissions


    def count_submissions(self):
        return len(self.submissions)