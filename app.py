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


main_view = MainView()

student_repo = StudentRepo()
student_controller = StudentController(student_repo)
student_view = StudentView(student_controller)

teacher_repo = TeacherRepo()
teacher_controller = TeacherController(teacher_repo)
teacher_view = TeacherView(teacher_controller)

course_repo = CourseRepo()
course_controller = CourseController(course_repo, teacher_repo)
course_view = CourseView(course_controller)

exercise_repo = ExerciseRepo()
exercise_controller = ExerciseController(exercise_repo, course_repo)
exercise_view = ExerciseView(exercise_controller)


notification_repo = NotificationRepo()
student_notification_repo = StudentNotificationRepo()

notification_controller = NotificationController(
    notification_repo,
    student_notification_repo,
    teacher_repo,
    student_repo
)

notification_view = NotificationView(notification_controller)


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
    elif choice == "7":
        notification_view.display_menu()
    elif choice == "0":
           break
    