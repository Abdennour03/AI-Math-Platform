from repositories.student_repository import StudentRepo
from models.student import Student

repo = StudentRepo()
student1 = Student(1, "Abdennour El allaoui", "abdennour@gmail.com", "124556", "0909485476", "M1")
student2 = Student(3, "ahmed smsar", "ahmed@gmail.com", "124556", "0908482471", "M1")
student3 = Student(4, "yssin hasan", "yassin@gmail.com", "124556", "0908482471", "M1")
student4 = Student(2, "Abdennour bn hassan", "yassin@gmail.com", "124556", "0908482471", "M1")

repo.add_student(student1)
repo.add_student(student2)
repo.add_student(student3)
repo.add_student(student4)

repo.update_student(4, full_name="Abdennour el mekkaoui")
for student in repo.get_all_student():
    print(student.full_name)

result = repo.search_student("ab")
print("------------------")
for i in result:
    print(i.full_name)

print(repo.count_student())

