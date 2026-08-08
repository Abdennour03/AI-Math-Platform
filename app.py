from views.main_view import MainView
from views.student_view import StudentView
from views.teacher_view import TeacherView
from controllers.student_controller import StudentController
from repositories.student_repository import StudentRepo
from repositories.teacher_repository import TeacherRepo
from controllers.teacher_controller import TeacherController


main_view = MainView()

student_repo = StudentRepo()
student_controller = StudentController(student_repo)
student_view = StudentView(student_controller)

teacher_repo = TeacherRepo()
teacher_controller = TeacherController(teacher_repo)
teacher_view = TeacherView(teacher_controller)

while True:
    choice = main_view.display_menu()
    if choice == "1":
            student_view.display_menu()
    elif choice == "2":
            teacher_view.display_menu()
    elif choice == "0":
           break
    