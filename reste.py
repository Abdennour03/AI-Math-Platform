from database.database import Database
from repositories.course_repository import CourseRepo
from repositories.teacher_repository import TeacherRepo
from controllers.course_controller import CourseController

db = Database()

teacher_repo = TeacherRepo(db)
course_repo = CourseRepo(db)

course_controller = CourseController(
    course_repo,
    teacher_repo
)

courses = course_controller.get_courses_by_level("1BAC")

print(courses)