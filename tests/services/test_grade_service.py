import pytest

from database.database import Database
from models.course import Course
from models.exercise import Exercise
from models.student import Student
from models.teacher import Teacher
from repositories.course_repository import CourseRepo
from repositories.exercise_repository import ExerciseRepo
from repositories.grade_repository import GradeRepo
from repositories.student_repository import StudentRepo
from repositories.submission_repository import SubmissionRepo
from repositories.teacher_repository import TeacherRepo
from services.grade_service import GradeService


@pytest.fixture
def grade_context(tmp_path):
    db = Database(str(tmp_path / "grades.db"))
    students = StudentRepo(db)
    teachers = TeacherRepo(db)
    courses = CourseRepo(db)
    exercises = ExerciseRepo(db)
    grades = GradeRepo(db, students, exercises)
    teacher = Teacher(None, "Teacher", "teacher@example.com", "hash", "1")
    other_teacher = Teacher(None, "Other", "other@example.com", "hash", "1")
    student = Student(None, "Student", "student@example.com", "hash", "1", "A")
    teachers.add_teacher(teacher)
    teachers.add_teacher(other_teacher)
    students.add_student(student)
    course = Course(None, "Course", teacher, "A", "1")
    courses.add_course(course)
    exercise = Exercise(None, "Exercise", course)
    exercises.add_exercise(exercise)
    yield GradeService(grades, students, exercises, courses), teacher, other_teacher, student, exercise, grades, exercises
    db.close()


def test_grade_lifecycle_and_duplicate_rule(grade_context):
    service, teacher, _, student, exercise, grades, _ = grade_context
    service.create_grade(15, student.student_id, exercise.exercise_id, teacher.teacher_id)
    with pytest.raises(ValueError, match="already has a grade"):
        service.create_grade(16, student.student_id, exercise.exercise_id, teacher.teacher_id)
    service.update_grade_by_teacher(1, teacher.teacher_id, 18)
    assert grades.get_grade(1).score == 18


def test_teacher_cannot_grade_another_teachers_exercise(grade_context):
    service, _, other_teacher, student, exercise, _, _ = grade_context
    with pytest.raises(ValueError, match="own exercises"):
        service.create_grade(15, student.student_id, exercise.exercise_id, other_teacher.teacher_id)


def test_grade_score_uses_exercise_max_score(grade_context):
    service, teacher, _, student, exercise, _, exercise_repo = grade_context
    exercise_repo.update_exercise(exercise.exercise_id, max_score=10)
    with pytest.raises(ValueError, match="between 0 and 10"):
        service.create_grade(11, student.student_id, exercise.exercise_id, teacher.teacher_id)


def test_teacher_cannot_grade_before_student_submits(tmp_path):
    db = Database(str(tmp_path / "submission-required.db"))
    students = StudentRepo(db)
    teachers = TeacherRepo(db)
    courses = CourseRepo(db)
    exercises = ExerciseRepo(db)
    submissions = SubmissionRepo(db, students, exercises)
    grades = GradeRepo(db, students, exercises)

    teacher = Teacher(None, "Teacher", "teacher@example.com", "hash", "1")
    student = Student(None, "Student", "student@example.com", "hash", "1", "A")
    teachers.add_teacher(teacher)
    students.add_student(student)
    course = Course(None, "Course", teacher, "A", "1")
    courses.add_course(course)
    exercise = Exercise(None, "Exercise", course, 20)
    exercises.add_exercise(exercise)

    service = GradeService(grades, students, exercises, courses, submissions)

    with pytest.raises(ValueError, match="must submit the exercise"):
        service.create_grade(15, student.student_id, exercise.exercise_id, teacher.teacher_id)

    db.close()
