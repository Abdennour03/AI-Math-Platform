class TeacherRepo:
    def __init__(self):
        self.teachers = []
        self.next_id = 1

    def add_teacher(self, teacher):
        teacher.teacher_id = self.next_id
        self.next_id += 1
        self.teachers.append(teacher)

    def get_teacher(self, teacher_id):
        for teacher in self.teachers:
            if teacher.teacher_id == teacher_id:
                return teacher
        return None
    
    def get_all_teachers(self):
        return self.teachers
        
    def update_teacher(self, teacher_id, **kwargs):
        for teacher in self.teachers:
            if teacher.teacher_id == teacher_id:
                for key, value in kwargs.items():
                    if hasattr(teacher, key):
                        setattr(teacher, key, value)
                return True 
        return False

    def delete_teacher(self, teacher_id):
        for index, teacher in enumerate(self.teachers):
            if teacher.teacher_id == teacher_id:
                del self.teachers[index]
                return True
        return False
        
    def search_teacher(self, full_name):
        results = []
        for teacher in self.teachers:
            if full_name.lower() in teacher.full_name.lower():
                results.append(teacher)
        return results

    
    def count_teacher(self):
        return len(self.teachers)
