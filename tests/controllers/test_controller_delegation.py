from controllers.course_controller import CourseController


def test_course_controller_delegates_to_service():
    class Service:
        def count_courses(self):
            return 3

    assert CourseController(Service()).count_courses() == 3
