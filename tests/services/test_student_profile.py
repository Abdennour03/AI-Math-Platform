from models.student import Student
from services.student_service import StudentService


class StudentRepository:
    def __init__(self, student):
        self.student = student

    def get_student(self, student_id):
        return self.student


def test_student_profile_includes_class_id():
    student = Student(
        1,
        "Yassin",
        "yassin@example.com",
        "hash",
        "0679120023",
        "3AC",
        1,
    )
    service = StudentService(StudentRepository(student), None)

    profile = service.get_my_profile(student)

    assert profile["class_id"] == 1