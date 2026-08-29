from models.student import Student
from utils.student_validation import StudentValidator
from utils.security import hash_password
class StudentController:
    def __init__(self, student_repo):
        self.student_repo = student_repo
        
    def create_student(self, full_name, email, password, phone_number, level):
        validation = StudentValidator()
        validation.validate_name(full_name)
        validation.validate_email(email)
        validation.validate_password(password)
        validation.validate_phone_number(phone_number)
        validation.validate_level(level)
        hashed_password = hash_password(password)
        student = Student(None, full_name, email, hashed_password, phone_number, level)
        self.student_repo.add_student(student)
        return student
        

    def get_student(self, student_id):
        if not isinstance(student_id, int):
            raise ValueError("student Id must be an integer.")
        student = self.student_repo.get_student(student_id)
        if student is None:
            raise ValueError("student not found.")
        return student

    def get_all_students(self):
        students = self.student_repo.get_all_student()
        if not students:
            raise ValueError("No students found.")
        return students
    
    def update_student(self, student_id, **kwargs):
        student = self.student_repo.get_student(student_id)
        if student is None:
            raise ValueError("studentnot found.")
        if "full_name" in kwargs:
            StudentValidator.validate_name(kwargs["full_name"])
            
        if "email" in kwargs:
            StudentValidator.validate_email(kwargs["email"])

        if "password" in kwargs:
            StudentValidator.validate_password(kwargs["password"])
            kwargs["password"] = hash_password(kwargs["password"])

        if "phone_number" in kwargs:
            StudentValidator.validate_phone_number(kwargs["phone_number"])
        if "level" in kwargs:
            StudentValidator.validate_level(kwargs["level"])

        self.student_repo.update_student(student_id, **kwargs)
        return "Student updated successfully"

    def delete_student(self, student_id):
        if not isinstance(student_id, int):
            raise ValueError("Student ID must be an integer")
        student = self.student_repo.get_student(student_id)
        if student is None:
            raise ValueError("Student is not found.")
        self.student_repo.delete_student(student_id)
        return "Student deleted successfully."
    
    def search_student(self, full_name):
        StudentValidator.validate_name(full_name)
        students = self.student_repo.search_student(full_name)
        if not students:
            raise ValueError("No students found.")
        return students

    def count_students(self):
        return self.student_repo.count_students()