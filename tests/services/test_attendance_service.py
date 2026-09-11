from datetime import date

import pytest

from database.database import Database
from models.class_group import ClassGroup
from models.student import Student
from models.teacher import Teacher
from repositories.attendance_repository import AttendanceRepo
from repositories.class_repository import ClassRepo
from repositories.student_repository import StudentRepo
from repositories.teacher_repository import TeacherRepo
from services.attendance_service import AttendanceService
from services.class_service import ClassService


@pytest.fixture
def attendance_context(tmp_path):
    db = Database(str(tmp_path / "attendance.db"))
    teacher_repo = TeacherRepo(db)
    class_repo = ClassRepo(db)
    student_repo = StudentRepo(db)
    class_service = ClassService(class_repo)
    attendance_repo = AttendanceRepo(db)
    teacher = Teacher(None, "Teacher", "teacher@example.com", "hash", "phone")
    teacher_repo.add_teacher(teacher)
    class_group = ClassGroup(None, "3AC", "2026")
    class_repo.add_class(class_group)
    teacher_repo.assign_teacher_to_classes(teacher.teacher_id, [class_group.class_id])
    first_student = Student(None, "First", "first@example.com", "hash", "phone", "3AC", class_group.class_id)
    second_student = Student(None, "Second", "second@example.com", "hash", "phone", "3AC", class_group.class_id)
    student_repo.add_student(first_student)
    student_repo.add_student(second_student)
    service = AttendanceService(attendance_repo, teacher_repo, class_service)
    yield db, service, teacher, class_group, first_student, second_student
    db.close()


def test_save_attendance_and_update_same_day(attendance_context):
    db, service, teacher, class_group, first_student, second_student = attendance_context
    records = [
        {"student_id": first_student.student_id, "status": "present"},
        {"student_id": second_student.student_id, "status": "absent"},
    ]

    service.save_attendance(teacher.teacher_id, class_group.class_id, date(2026, 9, 11), records)
    service.save_attendance(
        teacher.teacher_id,
        class_group.class_id,
        date(2026, 9, 11),
        [{"student_id": second_student.student_id, "status": "present"}],
    )

    rows = db.cursor.execute(
        "SELECT student_id, status FROM attendance ORDER BY student_id"
    ).fetchall()
    assert rows == [
        (first_student.student_id, "present"),
        (second_student.student_id, "present"),
    ]


def test_attendance_rejects_student_from_another_class(attendance_context):
    db, service, teacher, class_group, first_student, _ = attendance_context
    other_class = ClassGroup(None, "1BAC", "2026")
    ClassRepo(db).add_class(other_class)
    other_student = Student(None, "Other", "other@example.com", "hash", "phone", "1BAC", other_class.class_id)
    StudentRepo(db).add_student(other_student)

    with pytest.raises(ValueError, match="belong to the selected class"):
        service.save_attendance(
            teacher.teacher_id,
            class_group.class_id,
            date(2026, 9, 11),
            [{"student_id": other_student.student_id, "status": "present"}],
        )

    assert db.cursor.execute("SELECT COUNT(*) FROM attendance").fetchone()[0] == 0


def test_teacher_history_filters_by_month(attendance_context):
    _, service, teacher, class_group, first_student, _ = attendance_context
    service.save_attendance(
        teacher.teacher_id,
        class_group.class_id,
        date(2026, 9, 11),
        [{"student_id": first_student.student_id, "status": "present"}],
    )

    history = service.get_teacher_history(teacher.teacher_id, month="2026-09")

    assert len(history) == 1
    assert history[0]["student_id"] == first_student.student_id
    assert history[0]["status"] == "present"
