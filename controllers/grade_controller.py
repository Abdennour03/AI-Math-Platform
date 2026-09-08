class GradeController:
    def __init__(self, grade_service):
        self.grade_service = grade_service

    def create_grade(self, score, student_id, exercise_id, teacher_id=None):
        return self.grade_service.create_grade(
            score, student_id, exercise_id, teacher_id
        )

    def get_grade(self, grade_id):
        return self.grade_service.get_grade(grade_id)

    def get_all_grades(self):
        return self.grade_service.get_all_grades()

    def update_grade(self, grade_id, **kwargs):
        return self.grade_service.update_grade(grade_id, **kwargs)

    def delete_grade(self, grade_id):
        return self.grade_service.delete_grade(grade_id)

    def delete_grade_by_teacher(self, grade_id, teacher_id):
        return self.grade_service.delete_grade_by_teacher(grade_id, teacher_id)

    def search_grade_by_student(self, student_id):
        return self.grade_service.search_grade_by_student(student_id)

    def search_grade_by_exercise(self, exercise_id):
        return self.grade_service.search_grade_by_exercise(exercise_id)

    def count_grades(self):
        return self.grade_service.count_grades()

    def get_grades_by_student(self, student_id):
        return self.grade_service.get_grades_by_student(student_id)

    def get_grades_by_teacher(self, teacher_id):
        return self.grade_service.get_grades_by_teacher(teacher_id)

    def update_grade_by_teacher(self, grade_id, teacher_id, score):
        return self.grade_service.update_grade_by_teacher(grade_id, teacher_id, score)