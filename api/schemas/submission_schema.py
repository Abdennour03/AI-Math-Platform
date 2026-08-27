from pydantic import BaseModel
from datetime import datetime


class SubmissionCreate(BaseModel):
    exercise_id: int
    file_path: str

class SubmissionUpdate(BaseModel):
    submission_date: datetime | None = None
    file_path: str | None = None
    status: str | None = None


class SubmissionResponse(BaseModel):
    submission_id: int
    student_id: int
    exercise_id: int
    submission_date: datetime
    file_path: str
    status: str