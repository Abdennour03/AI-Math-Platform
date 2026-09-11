from pydantic import BaseModel


class CourseResponse(BaseModel):
    course_id: int
    course_name: str
    teacher_id: int
    level: str
    semester: str
    


class CourseCreate(BaseModel):
    course_name: str
    teacher_id: int | None = None
    level: str
    semester: str


class TeacherCourseCreate(BaseModel):
    course_name: str
    class_id: int
    semester: str
    


class CourseUpdate(BaseModel):
    course_name: str | None = None
    teacher_id: int | None = None
    level: str | None = None
    semester: str | None = None
    