from fastapi import APIRouter, Depends, HTTPException, Query

from api.dependencies import (
    attendance_controller,
    get_current_admin,
    require_teacher,
)
from api.schemas.attendance_schema import AttendanceSaveRequest

router = APIRouter(tags=["Attendance"])


def attendance_response(record):
    return {
        "student_id": record["student_id"],
        "student_name": record.get("student_name"),
        "class_id": record["class_id"],
        "date": record["date"],
        "status": record["status"],
    }


@router.get("/teachers/me/attendance/classes/{class_id}/students")
def get_class_students_for_attendance(
    class_id: int,
    current_user=Depends(require_teacher),
):
    try:
        return attendance_controller.get_class_students(current_user.teacher_id, class_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/teachers/me/attendance")
def save_attendance(
    data: AttendanceSaveRequest,
    current_user=Depends(require_teacher),
):
    try:
        return attendance_controller.save_attendance(
            current_user.teacher_id,
            data.class_id,
            data.date,
            [record.model_dump() for record in data.records],
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/teachers/me/attendance")
def get_teacher_attendance_history(
    class_id: int | None = None,
    month: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
    current_user=Depends(require_teacher),
):
    try:
        records = attendance_controller.get_teacher_history(
            current_user.teacher_id, class_id, month
        )
        return [attendance_response(record) for record in records]
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/admin/attendance/report")
def get_monthly_attendance_report(
    class_id: int,
    month: str = Query(pattern=r"^\d{4}-\d{2}$"),
    _admin=Depends(get_current_admin),
):
    try:
        records = attendance_controller.get_monthly_report(class_id, month)
        return [attendance_response(record) for record in records]
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
