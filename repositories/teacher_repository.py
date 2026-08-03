class TeacherRepo:
    def __init__(self):
        self.teacher = []

    def add_teacher(self, teacher):
        self.teacher.append(teacher)

    def get_teacher(self, teacher_id):
        for teacher in self.teacher:
            if teacher.teacher_id == teacher_id:
                return teacher
        return None
    
    def get_all_teacher(self):
        return self.teacher
        
    def update_teacher(self, teacher_id, **kwargs):
        for teacher in self.teacher:
            if teacher.teacher_id == teacher_id:
                for key, value in kwargs.items():
                    if hasattr(teacher, key):
                        setattr(teacher, key, value)
                return True 
        return False

    def delete_teacher(self, teacher_id):
        for index, teacher in enumerate(self.teacher):
            if teacher.teacher_id == teacher_id:
                del self.teacher[index]
                return True
        return False
        
    def search_teacher(self, full_name):
        results = []
        for teacher in self.teacher:
            if full_name.lower() in teacher.full_name.lower():
                results.append(teacher)
        return results

    
    def count_teacher(self):
        return len(self.teacher)
