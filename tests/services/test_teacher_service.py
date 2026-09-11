import pytest
from types import SimpleNamespace

from database.database import Database
from models.class_group import ClassGroup
from models.teacher import Teacher
from repositories.class_repository import ClassRepo
from repositories.teacher_repository import TeacherRepo
from services.admin_service import AdminService
from services.class_service import ClassService
from services.teacher_service import TeacherService


@pytest.fixture
def teacher_context(tmp_path):
    db = Database(str(tmp_path / "teachers.db"))
    teachers = TeacherRepo(db)
    classes = ClassRepo(db)
    first_teacher = Teacher(None, "First Teacher", "first@example.com", "hash", "1")
    second_teacher = Teacher(None, "Second Teacher", "second@example.com", "hash", "1")
    teachers.add_teacher(first_teacher)
    teachers.add_teacher(second_teacher)
    class_group = ClassGroup(None, "Class A", "2026")
    classes.add_class(class_group)
    yield TeacherService(teachers), first_teacher, second_teacher, class_group
    db.close()


def test_class_cannot_be_assigned_to_two_teachers(teacher_context):
    service, first_teacher, second_teacher, class_group = teacher_context
    service.assign_to_classes(first_teacher.teacher_id, [class_group.class_id])

    with pytest.raises(ValueError, match="already assigned to another teacher"):
        service.assign_to_classes(second_teacher.teacher_id, [class_group.class_id])

    assert service.get_teacher(first_teacher.teacher_id).classes[0].class_id == class_group.class_id


@pytest.fixture
def admin_teacher_context(tmp_path):
    db = Database(str(tmp_path / "admin-teachers.db"))
    teacher_repo = TeacherRepo(db)
    class_service = ClassService(ClassRepo(db))
    teacher_service = TeacherService(teacher_repo)
    admin_service = AdminService(None, None, teacher_service, class_service)
    yield db, admin_service, teacher_service, class_service
    db.close()


def teacher_data(class_ids):
    return SimpleNamespace(
        full_name="New Teacher",
        email="new.teacher@example.com",
        password="password1",
        phone_number="0600000000",
        class_ids=class_ids,
    )


def test_invalid_class_does_not_create_teacher(admin_teacher_context):
    db, admin_service, _, _ = admin_teacher_context

    with pytest.raises(ValueError, match="Class not found"):
        admin_service.create_teacher(teacher_data([999]))

    assert db.cursor.execute("SELECT COUNT(*) FROM teachers").fetchone()[0] == 0


def test_occupied_class_does_not_create_teacher(admin_teacher_context):
    db, admin_service, teacher_service, class_service = admin_teacher_context
    class_group = class_service.create_class("Class A", "2026")
    existing_teacher = teacher_service.create_teacher(
        "Existing Teacher", "existing@example.com", "password1", "0600000001"
    )
    teacher_service.assign_to_classes(existing_teacher.teacher_id, [class_group.class_id])

    with pytest.raises(ValueError, match="already assigned to another teacher"):
        admin_service.create_teacher(teacher_data([class_group.class_id]))

    assert db.cursor.execute("SELECT COUNT(*) FROM teachers").fetchone()[0] == 1