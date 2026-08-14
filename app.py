from views.main_view import MainView
from views.student_view import StudentView
from views.teacher_view import TeacherView
from controllers.student_controller import StudentController
from repositories.student_repository import StudentRepo
from repositories.teacher_repository import TeacherRepo
from controllers.teacher_controller import TeacherController

from views.course_view import CourseView
from controllers.course_controller import CourseController
from repositories.course_repository import CourseRepo

from views.exercise_view import ExerciseView
from controllers.exercise_controller import ExerciseController
from repositories.exercise_repository import ExerciseRepo


from repositories.notification_repository import NotificationRepo
from repositories.student_notification_repository import StudentNotificationRepo

from controllers.notification_controller import NotificationController
from views.notification_view import NotificationView

from views.submission_view import SubmissionView
from controllers.submission_controller import SubmissionController
from repositories.submission_repository import SubmissionRepo

from views.grade_view import GradeView
from controllers.grade_controller import GradeController
from repositories.grade_repository import GradeRepo

from database.database import Database
db = Database()
db.create_tables()
main_view = MainView()

# notification repos
student_repo = StudentRepo(db)
notification_repo = NotificationRepo(db)
student_notification_repo = StudentNotificationRepo(
    db,
    student_repo,
    notification_repo
)

student_controller = StudentController(student_repo)

teacher_repo = TeacherRepo(db)
teacher_controller = TeacherController(teacher_repo)
teacher_view = TeacherView(teacher_controller)

notification_controller = NotificationController(
    notification_repo,
    student_notification_repo,
    teacher_repo,
    student_repo
)
student_view = StudentView(student_controller, notification_controller)

course_repo = CourseRepo(db)
course_controller = CourseController(course_repo, teacher_repo)
course_view = CourseView(course_controller)

exercise_repo = ExerciseRepo(db)
exercise_controller = ExerciseController(exercise_repo, course_repo)
exercise_view = ExerciseView(exercise_controller)

notification_controller = NotificationController(
    notification_repo,
    student_notification_repo,
    teacher_repo,
    student_repo
)
notification_view = NotificationView(notification_controller)

submission_repo = SubmissionRepo(db, student_repo, exercise_repo)
submission_controller = SubmissionController(
    submission_repo,
    student_repo,
    exercise_repo
)
submission_view = SubmissionView(submission_controller)


grade_repo = GradeRepo(db, student_repo, exercise_repo)

grade_controller = GradeController(
    grade_repo,
    student_repo,
    exercise_repo
)

grade_view = GradeView(
    grade_controller
)

while True:
    choice = main_view.display_menu()
    if choice == "1":
            student_view.display_menu()
    elif choice == "2":
            teacher_view.display_menu()
    elif choice == "3":
            course_view.display_menu()
    elif choice == "4":
            exercise_view.display_menu()
    elif choice == "5":
        grade_view.display_menu()
    elif choice == "6":
        submission_view.display_menu()
    elif choice == "7":
        notification_view.display_menu()
    elif choice == "0":
    
           break
    