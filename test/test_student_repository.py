from repositories.student_repository import StudentRepo
from models.student import Student

repo = StudentRepo()
student1 = Student(1, "Abdennour", "abdennour@gmail.com", "124556", "0909485476", "M1")
student2 = Student(3, "ahmed", "ahmed@gmail.com", "124556", "0908482471", "M1")
student3 = Student(4, "yssin", "yassin@gmail.com", "124556", "0908482471", "M1")

repo.add_student(student1)
repo.add_student(student2)
repo.add_student(student3)

print(student3.student_id)
result = repo.get_student(4)
print(result.full_name)
