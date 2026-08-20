from pydantic import BaseModel


class ExerciseResponse(BaseModel):
    exercise_id: int
    exercise_name: str
    course_id: int
    level: str


class ExerciseCreate(BaseModel):
    exercise_name: str
    course_id: int
    level: str


class ExerciseUpdate(BaseModel):
    exercise_name: str | None = None
    course_id: int | None = None
    level: str | None = None