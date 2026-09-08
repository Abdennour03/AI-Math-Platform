class SubmissionController:
    def __init__(self, submission_service):
        self.submission_service = submission_service

    def create_submission(self, student_id, exercise_id, file_path):
        return self.submission_service.create_submission(student_id, exercise_id, file_path)

    def get_submission(self, submission_id):
        return self.submission_service.get_submission(submission_id)

    def get_all_submissions(self):
        return self.submission_service.get_all_submissions()

    def update_submission(self, submission_id, **kwargs):
        return self.submission_service.update_submission(submission_id, **kwargs)

    def delete_submission(self, submission_id):
        return self.submission_service.delete_submission(submission_id)

    def search_submission_by_student(self, student_id):
        return self.submission_service.search_submission_by_student(student_id)

    def search_submission_by_exercise(self, exercise_id):
        return self.submission_service.search_submission_by_exercise(exercise_id)

    def count_submissions(self):
        return self.submission_service.count_submissions()

    def get_submissions_by_student(self, student_id):
        return self.submission_service.get_submissions_by_student(student_id)

    def get_submissions_by_teacher(self, teacher_id):
        return self.submission_service.get_submissions_by_teacher(teacher_id)