from repositories.teacher_repository import TeacherRepo
from models.teacher import Teacher


teacher1 = Teacher(1, "Pr.Abdennour","abdennour@gmail.com", "hdjddif4", "090886643" )
teacher2 = Teacher(2, "Pr.mohamed","mohamed@gmail.com", "hdjddif4", "080886643" )

repo = TeacherRepo()
repo.add_teacher(teacher1)
repo.add_teacher(teacher2)

result = repo.get_teacher(1)
print(repo.count_teacher())
print(result.full_name)