class StudentRepo:
    def __init__(self):
        self.student = []
    def add_student(self, student):
        self.student.append(student)

    def get_student(self, student_id):
        for student in self.student:
            if student.student_id == student_id:
                return student
        return None
    def get_all_student(self, student):
        pass
    def update_student(self, student):
        pass
    def delete_student(self, student):
        pass
    def search_student(self, student):
        pass
    def count_student(self, student):
        pass