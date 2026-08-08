class StudentRepo:
    def __init__(self):
        self.students = []
        self.next_id = 1
        
    def add_student(self, student):
        student.student_id = self.next_id
        self.next_id += 1
        self.students.append(student)

    def get_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def get_all_student(self):
        return self.students
        
    def update_student(self, student_id, **kwargs):
        for student in self.students:
            if student.student_id == student_id:
                for key, value in kwargs.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                return True 
        return False

    def delete_student(self, student_id):
        for index, student in enumerate(self.students):
            if student.student_id == student_id:
                del self.students[index]
                return True
        return False
        
    def search_student(self, full_name):
        results = []
        for student in self.students:
            if full_name.lower() in student.full_name.lower():
                results.append(student)
        return results

    
    def count_students(self):
        return len(self.students)
