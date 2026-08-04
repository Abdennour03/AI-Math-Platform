from models.teacher import Teacher
from utils.teacher_validation import TeacherValidator

class TeacherController:
    def __init__(self, teacher_repo):
        self.teacher_repo = teacher_repo
        
    def create_teacher(self, full_name, email, password, phone_number):
        validation = TeacherValidator()
        validation.validate_name(full_name)
        validation.validate_email(email)
        validation.validate_password(password)
        validation.validate_phone_number(phone_number)
        teacher = Teacher(None, full_name, email, password, phone_number)
        self.teacher_repo.add_teacher(teacher)
        return "teacher created successfuly."
        

    def get_teacher(self, teacher_id):
        if not isinstance(teacher_id, int):
            raise ValueError("Teacher Id must be an integer.")
        teacher = self.teacher_repo.get_teacher(teacher_id)
        if teacher in None:
            raise ValueError("Teacher not found.")
        return teacher


    def get_all_teachers(self):
            teachers = self.teacher_repo.get_all_teacher()
            if not teachers:
                raise ValueError("No teachers found.")
            return teachers
        
    def update_teacher(self, teacher_id, **kwargs):
            teacher = self.teacher_repo.get_teacher(teacher_id)
            if teacher is None:
                raise ValueError("teachernot found.")
            if "full_name" in kwargs:
                TeacherValidator.validate_name(kwargs["full_name"])
            if "email" in kwargs:
                TeacherValidator.validate_name(kwargs["email"])
            if "password" in kwargs:
                TeacherValidator.validate_name(kwargs["password"])
            if "phone_number" in kwargs:
                TeacherValidator.validate_name(kwargs["phone_number"])
            if "level" in kwargs:
                TeacherValidator.validate_name(kwargs["level"])
    
            self.teacher_repo.update_teacher(teacher_id, **kwargs)
            return "teacher updated successfully"
    
    def delete_teacher(self, teacher_id):
            if not isinstance(teacher_id, int):
                raise ValueError("teacher ID must be an integer")
            teacher = self.teacher_repo.get_teacher(teacher_id)
            if teacher is None:
                raise ValueError("teacher is not found.")
            self.teacher_repo.delete_teacher(teacher_id)
            return "teacher deleted successfully."
        
    def search_teacher(self, full_name):
            TeacherValidator.validate_name(full_name)
            teachers = self.teacher_repo.search_teacher(full_name)
            if not teachers:
                raise ValueError("No teachers found.")
            return teachers
    
    def count_teachers(self):
            return self.teacher_repo.count_teacher()