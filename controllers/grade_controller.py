from models.grad import Grade
from models.student import Student
from models.exercise import Exercise
from utils.grade_validation import GradeValidator

class GradeController:
    def __init__(self, grade_repo, student_repo, exercise_repo):
        self.grade_repo = grade_repo
        self.student_repo = student_repo
        self.exercise_repo = exercise_repo

    def create_grade(self, score, student_id, exercise_id):
        # check if the student and exercise from Student and Exercise model 
        GradeValidator.validation_score(score)
        if not isinstance(student_id, int):
            raise ValueError("Invalid student.")
        if not isinstance(exercise_id, Exercise):
            raise ValueError("Invalid exercise")
        student = self.student_repo.get_student(student_id)
        if student is None:
            raise ValueError("Student not found.")

        exercise = self.exercise_repo.get_exercise(exercise_id)
        if exercise is None:
            raise ValueError("exercise not found.")
        # create grade
        grade = Grade(None, score, student, exercise)
        # add the grade
        self.grade_repo.add_grade(grade)
        return "Grade created successfully."

    def get_grade(self, grade_id):
        if not isinstance(grade_id, int):
            raise ValueError("Grade ID must be an int")
        grade = self.grade_repo.get_grade(grade_id)
        if grade is None:
            raise ValueError("Grade not found.")
        return grade

    def get_all_grades(self):
        return self.grade_repo.get_all_grades()

    def update_grade(self, grade_id, **kwargs):
        grade = self.grade_repo.get_grade(grade_id)
        if grade is None:
            raise ValueError("grade not found")
        if "score" in kwargs:
            GradeValidator.validation_score(kwargs["score"])

        self.grade_repo.update_grade(grade_id, **kwargs)
        return "Grade updated succssfully."
        
        

    def delete_grade(self, grade_id):

        grade = self.grade_repo.get_grade(grade_id)
        if grade is None:
            raise ValueError("Grade is nout Found .")
        self.grade_repo.delete_grade(grade_id)
        return "Grade deleted succssfully ."

    def search_grade_by_student(self, student_id):
        #chech if student_id is integer
        if not isinstance(student_id, int):
            raise ValueError("Student ID must be int.")

        #check if grade of student if found and return it 
        grades = self.grade_repo.search_grade_by_student(student_id)
        if not grades :
            raise ValueError("No grade found.")
        return grades
    def search_grade_by_exercise(self, exercise_id):
        if not isinstance(exercise_id, int):
            raise ValueError("exercise ID must be int.")
        
        #check if grade of student if found and return it 
        grades = self.grade_repo.search_grade_by_exercise(exercise_id)
        if not grades :
            raise ValueError("No grade found.")
        return grades

    def count_grades(self):
        return self.grade_repo.count_grades()
