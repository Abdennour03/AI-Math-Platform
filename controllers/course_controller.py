from models.course import Course
from utils.validation_course import CourseValidator

class CourseController:
    def __init__(self, course_repo, teacher_repo):
        self.course_repo = course_repo
        self.teacher_repo = teacher_repo

    def create_course(self, course_name, teacher_id, level, semester):

        CourseValidator.validate_course_name(course_name)
        CourseValidator.Validation_level(level)
        CourseValidator.Validation_semester(semester)
        
        teacher = self.teacher_repo.get_teacher(teacher_id)
        if teacher is None:
            raise ValueError("Teacher not found")
        course = Course(None, course_name, teacher, level, semester)

        self.course_repo.add_course(course)
        return "Course created successfully."

    def get_course(self, course_id):

        if not isinstance(course_id, int):
            raise ValueError("Course ID must be an int")
        course = self.course_repo.get_course(course_id)
        if course is None:
            raise ValueError("Course not found.")
        return course

    def get_all_courses(self):
        return self.course_repo.get_all_courses()

    def update_course(self, course_id, **kwargs):
        course = self.course_repo.get_course(course_id)
        if course is None :
            raise ValueError("Course not found")
        if "course_name" in kwargs:
            CourseValidator.validate_course_name(kwargs["course_name"])
        if "teacher_id" in kwargs:
            teacher = self.teacher_repo.get_teacher(kwargs["teacher_id"])
            if teacher is None:
                raise ValueError("Teacher not found.")
            kwargs["teacher"] = teacher
            del kwargs["teacher_id"] 

        self.course_repo.update_course(course_id, **kwargs)
        return "Course updated successfully."
    def delete_course(self, course_id):
        course = self.course_repo.get_course(course_id)
        if course is None:
            raise ValueError('Course ID not found.')
        self.course_repo.delete_course(course_id)
        return "Course deleted successfully"

    def search_course(self, query):
        query = query.strip()
        if not query:
            raise ValueError("Search query cannot be empty.")

        courses = self.course_repo.search_course(query)
        if not courses:
            raise ValueError("No courses found.")
        return courses

    def count_courses(self):
        return self.course_repo.count_courses()