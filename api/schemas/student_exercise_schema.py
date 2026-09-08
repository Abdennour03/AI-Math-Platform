from pydantic import BaseModel


class StudentExerciseResponse(BaseModel):
    exercise_id: int
    exercise_name: str
    course: dict