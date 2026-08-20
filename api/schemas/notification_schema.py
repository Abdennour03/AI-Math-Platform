from pydantic import BaseModel


class NotificationResponse(BaseModel):
    notification_id: int
    title: str
    message: str
    teacher_id: int
    teacher_name: str
    created_at: str


class NotificationCreate(BaseModel):
    title: str
    message: str
    teacher_id: int
    student_id: int


class NotificationUpdate(BaseModel):
    title: str | None = None
    message: str | None = None
    teacher_id: int | None = None