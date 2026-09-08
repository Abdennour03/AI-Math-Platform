from database.database import Database
from models.course import Course
from models.exercise import Exercise
from models.grade import Grade
from models.student import Student
from models.teacher import Teacher
from repositories.course_repository import CourseRepo
from repositories.exercise_repository import ExerciseRepo
from repositories.grade_repository import GradeRepo
from repositories.student_repository import StudentRepo
from repositories.teacher_repository import TeacherRepo
from services.student_service import StudentService


def test_student_exercises_include_grade_or_none(tmp_path):
    db = Database(str(tmp_path / "student-exercises.db"))
    student_repo = StudentRepo(db)
    teacher_repo = TeacherRepo(db)
    course_repo = CourseRepo(db)
    exercise_repo = ExerciseRepo(db)
    grade_repo = GradeRepo(db, student_repo, exercise_repo)

    student = Student(None, "Student", "student@example.com", "hash", "1", "A")
    teacher = Teacher(None, "Teacher", "teacher@example.com", "hash", "1")
    student_repo.add_student(student)
    teacher_repo.add_teacher(teacher)

    course = Course(None, "Course", teacher, "A", "1")
    course_repo.add_course(course)
    graded_exercise = Exercise(None, "Graded", course, 20)
    ungraded_exercise = Exercise(None, "Ungraded", course, 20)
    exercise_repo.add_exercise(graded_exercise)
    exercise_repo.add_exercise(ungraded_exercise)
    grade_repo.add_grade(Grade(None, 17, student, graded_exercise))

    exercises = StudentService(student_repo, exercise_repo).get_my_exercises(
        student.student_id,
        student.level,
    )

    scores = {exercise.exercise_name: exercise.score for exercise in exercises}
    assert scores == {"Graded": 17.0, "Ungraded": None}
    db.close()
