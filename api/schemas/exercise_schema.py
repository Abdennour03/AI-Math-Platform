from pydantic import BaseModel


class ExerciseResponse(BaseModel):
    exercise_id: int
    exercise_name: str
    course_id: int
    max_score: float


class ExerciseCreate(BaseModel):
    exercise_name: str
    course_id: int
    max_score: float = 20


class TeacherExerciseCreate(BaseModel):
    exercise_name: str
    course_id: int
    max_score: float = 20


class ExerciseUpdate(BaseModel):
    exercise_name: str | None = None
    course_id: int | None = None
    max_score: float | None = None
