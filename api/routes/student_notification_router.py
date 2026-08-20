from fastapi import APIRouter, HTTPException

from api.dependencies import student_notification_repo


router = APIRouter(
    prefix="/student-notifications",
    tags=["student-notifications"]
)


@router.get(
    "/student/{student_id}",
    response_model=list[dict]
)
def get_notifications_for_student(student_id: int):

    notifications = (
        student_notification_repo
        .get_notifications_for_student(student_id)
    )

    return [
        {
            "student_notification_id":
                item.student_notification_id,

            "notification_id":
                item.notification.notification_id,

            "title":
                item.notification.title,

            "message":
                item.notification.message,

            "is_read":
                item.is_read,

            "created_at":
                item.notification.created_at
        }
        for item in notifications
    ]


@router.patch("/{student_notification_id}/read")
def mark_as_read(student_notification_id: int):

    result = student_notification_repo.mark_as_read(
        student_notification_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Student notification not found"
        )

    return {
        "message": "Notification marked as read"
    }