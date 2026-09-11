from database.database import Database
from models.class_group import ClassGroup
from models.course import Course
from models.exercise import Exercise
from models.student import Student
from models.teacher import Teacher
from repositories.class_repository import ClassRepo
from repositories.course_repository import CourseRepo
from repositories.exercise_repository import ExerciseRepo
from repositories.student_repository import StudentRepo
from repositories.teacher_repository import TeacherRepo
from services.student_service import StudentService


def test_exercises_are_found_by_student_class_id(tmp_path):
    db = Database(str(tmp_path / "student-exercises-class.db"))
    classes = ClassRepo(db)
    courses = CourseRepo(db)
    exercises = ExerciseRepo(db)
    students = StudentRepo(db)
    teachers = TeacherRepo(db)

    class_group = ClassGroup(None, "1BAC", "2026")
    classes.add_class(class_group)
    teacher = Teacher(None, "Teacher", "teacher@example.com", "hash", "1")
    teachers.add_teacher(teacher)
    course = Course(None, "Algebra", teacher, class_group.name, "S1")
    courses.add_course(course)
    exercise = Exercise(None, "Equation", course)
    exercises.add_exercise(exercise)
    student = Student(None, "Student", "student@example.com", "hash", "1", "3AC", class_group.class_id)
    students.add_student(student)

    result = StudentService(students, exercises).get_my_exercises(
        student.student_id,
        student.class_id,
    )

    assert [item.exercise_id for item in result] == [exercise.exercise_id]
    db.close()