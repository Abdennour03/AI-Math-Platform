from database.database import Database
from models.class_group import ClassGroup
from models.course import Course
from models.student import Student
from models.teacher import Teacher
from repositories.class_repository import ClassRepo
from repositories.course_repository import CourseRepo
from repositories.student_repository import StudentRepo
from repositories.teacher_repository import TeacherRepo
from services.course_service import CourseService


def test_courses_are_found_by_student_class_id(tmp_path):
    db = Database(str(tmp_path / "student-courses.db"))
    classes = ClassRepo(db)
    courses = CourseRepo(db)
    students = StudentRepo(db)
    teachers = TeacherRepo(db)

    class_group = ClassGroup(None, "1BAC", "2026")
    classes.add_class(class_group)
    teacher = Teacher(None, "Teacher", "teacher@example.com", "hash", "1")
    teachers.add_teacher(teacher)
    course = Course(None, "Algebra", teacher, class_group.name, "S1")
    courses.add_course(course)
    student = Student(None, "Student", "student@example.com", "hash", "1", "3AC", class_group.class_id)
    students.add_student(student)

    result = CourseService(courses, teachers).get_courses_by_class_id(student.class_id)

    assert [item.course_id for item in result] == [course.course_id]
    db.close()