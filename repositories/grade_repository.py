class GradeRepo:
    def __init__(self):
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def get_grade(self, grade_id):
        for grade in self.grades:
            if grade.grade_id == grade_id:
                return grade
        return None 


    def get_all_grades(self):
        return self.grades

    def update_grade(self, grade_id, **kwargs):
        for grade in self.grades:
            if grade.grade_id == grade_id:
                for key, value in kwargs.items():
                    if hasattr(grade, key):
                        setattr(grade, key, value)
                return True 
        return False

    def delete_grade(self, grade_id):
        for index, grade in enumerate(self.grades):
            if grade.grade_id == grade_id:
                del self.grades[index]
                return True
        return False

    def search_grade_by_student(self, student_id):
        result_grades = []
        for grade in self.grades:
            if grade.student.student_id == student_id:
                result_grades.append(grade)
        return result_grades

    
    def search_grade_by_exercises(self, exercise_id):
        result_grades = []
        for grade in self.grades:
            if grade.exercise.exercise_id == exercise_id:
                result_grades.append(grade)
        return result_grades

    def count_grades(self):
        return len(self.grades)