from repositories.teacher_repository import TeacherRepo
from models.teacher import Teacher
from controllers.teacher_controller import TeacherController


repo = TeacherRepo()
controller = TeacherController(repo)

controller.create_teacher(
    "abdennour el allaoui",
    "abdennoure03@gmail.com",
    "1233455t66",
    "0997879876",
)
controller.create_teacher(
    "amina el allaoui",
    "amina23@gmail.com",
    "1233455t66",
    "0797879876",
)
controller.create_teacher(
    "mohamed el allaoui",
    "mohamed034@gmail.com",
    "1233455t66",
    "0797879876",
)

print(controller.count_teachers())
print(controller.search_teacher("abd"))