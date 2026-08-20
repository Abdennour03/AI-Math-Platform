from pydantic import BaseModel


class StudentNotificationResponse(BaseModel):
    student_notification_id: int
    notification_id: int
    title: str
    message: str
    is_read: bool
    created_at: str