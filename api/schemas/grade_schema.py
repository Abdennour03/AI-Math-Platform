from pydantic import BaseModel


class GradeCreate(BaseModel):
    score: float
    student_id: int
    exercise_id: int


class GradeUpdate(BaseModel):
    score: float | None = None


class GradeResponse(BaseModel):
    grade_id: int
    score: float
    student_id: int
    exercise_id: int