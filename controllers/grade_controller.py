from models.grad import Grade
from utils.grade_validation import GradeValidator


class GradeController:

    def __init__(
        self,
        grade_repo,
        student_repo,
        exercise_repo,
        course_repo
    ):
        self.grade_repo = grade_repo
        self.student_repo = student_repo
        self.exercise_repo = exercise_repo
        self.course_repo = course_repo

    # =====================================================
    # CREATE GRADE
    # =====================================================

    def create_grade(self, score, student_id, exercise_id):

        GradeValidator.validation_score(score)

        if not isinstance(student_id, int):
            raise ValueError("Invalid student.")

        if not isinstance(exercise_id, int):
            raise ValueError("Invalid exercise.")

        student = self.student_repo.get_student(student_id)

        if student is None:
            raise ValueError("Student not found.")

        exercise = self.exercise_repo.get_exercise(exercise_id)

        if exercise is None:
            raise ValueError("Exercise not found.")

        existing_grade = self.grade_repo.get_grade_by_student_and_exercise(
            student_id,
            exercise_id
        )

        if existing_grade is not None:
            raise ValueError(
                "This student already has a grade for this exercise."
            )

        grade = Grade(
            None,
            score,
            student,
            exercise
        )

        self.grade_repo.add_grade(grade)

        return "Grade created successfully."

    # =====================================================
    # GET GRADE
    # =====================================================

    def get_grade(self, grade_id):

        if not isinstance(grade_id, int):
            raise ValueError("Grade ID must be an int.")

        grade = self.grade_repo.get_grade(grade_id)

        if grade is None:
            raise ValueError("Grade not found.")

        return grade

    # =====================================================
    # GET ALL GRADES
    # =====================================================

    def get_all_grades(self):

        return self.grade_repo.get_all_grades()

    # =====================================================
    # UPDATE GRADE
    # =====================================================

    def update_grade(self, grade_id, **kwargs):

        grade = self.grade_repo.get_grade(grade_id)

        if grade is None:
            raise ValueError("Grade not found.")

        if "score" in kwargs:
            GradeValidator.validation_score(
                kwargs["score"]
            )

        self.grade_repo.update_grade(
            grade_id,
            **kwargs
        )

        return "Grade updated successfully."

    # =====================================================
    # DELETE GRADE
    # =====================================================

    def delete_grade(self, grade_id):

        grade = self.grade_repo.get_grade(grade_id)

        if grade is None:
            raise ValueError("Grade not found.")

        self.grade_repo.delete_grade(grade_id)

        return "Grade deleted successfully."

    # =====================================================
    # SEARCH BY STUDENT
    # =====================================================

    def search_grade_by_student(self, student_id):

        if not isinstance(student_id, int):
            raise ValueError("Student ID must be int.")

        grades = self.grade_repo.search_grade_by_student(
            student_id
        )

        if not grades:
            raise ValueError("No grade found.")

        return grades

    # =====================================================
    # SEARCH BY EXERCISE
    # =====================================================

    def search_grade_by_exercise(self, exercise_id):

        if not isinstance(exercise_id, int):
            raise ValueError("Exercise ID must be int.")

        grades = self.grade_repo.search_grade_by_exercise(
            exercise_id
        )

        if not grades:
            raise ValueError("No grade found.")

        return grades

    # =====================================================
    # COUNT
    # =====================================================

    def count_grades(self):

        return self.grade_repo.count_grades()

    # =====================================================
    # GET GRADES BY STUDENT
    # =====================================================

    def get_grades_by_student(self, student_id):

        if not isinstance(student_id, int):
            raise ValueError("Student ID must be int.")

        student = self.student_repo.get_student(student_id)

        if student is None:
            raise ValueError("Student not found.")

        return self.grade_repo.search_grade_by_student(
            student_id
        )

    # =====================================================
    # GET GRADES BY TEACHER
    # =====================================================

    def get_grades_by_teacher(self, teacher_id):

        if not isinstance(teacher_id, int):
            raise ValueError("Teacher ID must be int.")

        return [
            grade
            for grade in self.grade_repo.get_all_grades()
            if grade.exercise.course.teacher.teacher_id == teacher_id
        ]

    # =====================================================
    # UPDATE GRADE BY TEACHER
    # =====================================================

    def update_grade_by_teacher(
        self,
        grade_id,
        teacher_id,
        score
    ):

        if not isinstance(grade_id, int):
            raise ValueError(
                "Grade ID must be an integer."
            )

        if not isinstance(teacher_id, int):
            raise ValueError(
                "Teacher ID must be an integer."
            )

        GradeValidator.validation_score(score)

        # Get grade
        grade = self.grade_repo.get_grade(grade_id)

        if grade is None:
            raise ValueError("Grade not found.")

        # Get exercise
        exercise = self.exercise_repo.get_exercise(
            grade.exercise.exercise_id
        )

        if exercise is None:
            raise ValueError("Exercise not found.")

        # Get course
        course = self.course_repo.get_course(
            exercise.course.course_id
        )

        if course is None:
            raise ValueError("Course not found.")

        # Check teacher ownership
        if course.teacher.teacher_id != teacher_id:
            raise ValueError(
                "You cannot update this grade."
            )

        # Update score
        self.grade_repo.update_grade(
            grade_id,
            score=score
        )

        return "Grade updated successfully."