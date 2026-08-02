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
    
    def get_all_student(self):
        return self.student
        
    def update_student(self, student_id, **kwargs):
        for index ,student in enumerate(self.student):
            if student.student_id == student_id:
                for key, value in kwargs.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                return True 
        return False

    def delete_student(self, student_id):
        for index, student in enumerate(self.student):
            if student.student_id == student_id:
                del self.student[index]
                return True
            return False
        
    def search_student(self, full_name):
        results = []
        for student in self.student:
            if full_name.lower() in student.full_name.lower():
                results.append(student)
        return results

    
    def count_student(self):
        return len(self.student)
