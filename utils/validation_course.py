class CourseValidator:
    @staticmethod
    def validate_course_name(course_name):
        course_name = course_name.strip()
        if not course_name:
            raise ValueError("Course name cannot be empty.")
        if len(course_name)<3 or len(course_name)>100:
            raise ValueError("Course name must contain at last 3 or not exceed 100 char...")


    @staticmethod
    def validate_description(description):
        description = description.strip()
        if not description:
            raise ValueError("Description cannot be empty")
    @staticmethod
    def Validation_level(level):
        if not isinstance(level, str) or not level.strip():
            raise ValueError("Class name is required.")
    @staticmethod
    def Validation_semester(semester):
        semester = semester.strip().upper()
        allowed_semesters = {"S1","S2",}
        if semester not in allowed_semesters:
            raise ValueError("Invalid semester.")