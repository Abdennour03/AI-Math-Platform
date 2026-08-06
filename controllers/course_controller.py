from models.course import Course
from utils.validation_course import CourseValidator
from models.teacher import Teacher

class CourseController:
    def __init__(self, course_repo):
        self.course_repo = course_repo

    def create_course(self, course_name, description, teacher, level, semester):

        CourseValidator.validate_course_name(course_name)
        CourseValidator.validate_description(description)
        CourseValidator.Validation_level(level)
        CourseValidator.Validation_semester(semester)

        
        if not isinstance(teacher, Teacher):
            raise ValueError("invalid teacher.")
        course = Course(None, course_name, description, teacher, level, semester)

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
        if "description" in kwargs:
             CourseValidator.validate_course_name(kwargs["description"])
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