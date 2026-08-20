from database.database import Database

from repositories.student_repository import StudentRepo
from controllers.student_controller import StudentController

from repositories.teacher_repository import TeacherRepo
from controllers.teacher_controller import TeacherController

from repositories.course_repository import CourseRepo
from controllers.course_controller import CourseController

from repositories.exercise_repository import ExerciseRepo
from controllers.exercise_controller import ExerciseController

from controllers.notification_controller import NotificationController
from repositories.notification_repository import NotificationRepo
from repositories.student_notification_repository import StudentNotificationRepo

from repositories.submission_repository import SubmissionRepo
from controllers.submission_controller import SubmissionController

from repositories.grade_repository import GradeRepo
from controllers.grade_controller import GradeController
db = Database()

# Student
student_repo = StudentRepo(db)
student_controller = StudentController(student_repo)

# Teacher
teacher_repo = TeacherRepo(db)
teacher_controller = TeacherController(teacher_repo)

# Course
course_repo = CourseRepo(db)
course_controller = CourseController(
    course_repo,
    teacher_repo
)

exercise_repo = ExerciseRepo(db)
exercise_controller = ExerciseController(exercise_repo, course_repo)

notification_repo = NotificationRepo(db)

student_notification_repo = StudentNotificationRepo(
    db,
    student_repo,
    notification_repo
)

notification_controller = NotificationController(
    notification_repo,
    student_notification_repo,
    teacher_repo,
    student_repo
)

submission_repo = SubmissionRepo(
    db,
    student_repo,
    exercise_repo
)
submission_controller = SubmissionController(
    submission_repo,
    student_repo,
    exercise_repo
)

grade_repo = GradeRepo(db, student_repo, exercise_repo)

grade_controller = GradeController(
    grade_repo,
    student_repo,
    exercise_repo
)