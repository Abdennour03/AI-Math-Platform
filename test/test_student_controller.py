from repositories.student_repository import StudentRepo
from controllers.student_controller import StudentController


repo = StudentRepo()
controller = StudentController(repo)


result = controller.create_student(
    "Abdennour",
    "abdennour@gmail.com ",
    "password123",
    "0612345678",
    "2BAC"

)
result = controller.create_student(
    "laila",
    " laila.@gmail.com",
    "password123",
    "0612345678",
    "3AC"

)
print(result)
print(controller.get_all_students())

print(controller.delete_student(1))