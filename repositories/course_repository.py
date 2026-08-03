class CourseRepo:
    def __init__(self):
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def get_course(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None 


    def get_all_courses(self):
        return self.courses

    def update_course(self, course_id, **kwargs):
        for course in self.courses:
            if course.course_id == course_id:
                for key, value in kwargs.items():
                    if hasattr(course, key):
                        setattr(course, key, value)
                return True 
        return False

    def delete_course(self, course_id):
        for index, course in enumerate(self.courses):
            if course.course_id == course_id:
                del self.courses[index]
                return True
        return False

    def search_course(self, query):
        result_courses = []
        for course in self.courses:
            if query.lower() in course.course_name.lower() :
                result_courses.append(course)
        return result_courses


    def count_courses(self):
        return len(self.courses)