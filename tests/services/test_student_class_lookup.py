from database.database import Database
from models.class_group import ClassGroup
from models.student import Student
from repositories.class_repository import ClassRepo
from repositories.student_repository import StudentRepo
from services.student_service import StudentService


def test_get_students_by_class_ids_returns_only_students_in_teacher_classes(tmp_path):
    db = Database(str(tmp_path / "students.db"))
    classes = ClassRepo(db)
    students = StudentRepo(db)
    first_class = ClassGroup(None, "Class A", "2026")
    second_class = ClassGroup(None, "Class B", "2026")
    classes.add_class(first_class)
    classes.add_class(second_class)
    first_student = Student(None, "First Student", "first@example.com", "hash", "1", "A", first_class.class_id)
    second_student = Student(None, "Second Student", "second@example.com", "hash", "1", "A", second_class.class_id)
    students.add_student(first_student)
    students.add_student(second_student)

    result = StudentService(students, None).get_students_by_class_ids([first_class.class_id])

    assert [student.student_id for student in result] == [first_student.student_id]
    db.close()