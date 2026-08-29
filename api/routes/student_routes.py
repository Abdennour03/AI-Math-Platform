from fastapi import APIRouter
from api.schemas.student_schema import (
    StudentResponse,
    StudentCreate,
    StudentUpdate
)
from api.dependencies import student_controller
from fastapi import APIRouter , HTTPException

router = APIRouter(
    prefix="/students",
    tags = ["Students"]
)
from fastapi import Depends
from api.dependencies import require_student


@router.get("/me", response_model=StudentResponse)
def get_my_profile(
    current_user=Depends(require_student)
):
    return {
        "student_id": current_user.student_id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone_number": current_user.phone_number,
        "level": current_user.level
    }
from api.dependencies import require_student
from fastapi import Depends
from api.dependencies import course_controller

@router.get("/me/courses")
def get_my_courses(
    current_user=Depends(require_student)
):
    courses = course_controller.get_courses_by_level(
        current_user.level
    )

    return [
        {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "semester": course.semester,
            "level": course.level,
            "teacher": {
                "teacher_id": course.teacher.teacher_id,
                "full_name": course.teacher.full_name
            }
        }
        for course in courses
    ]

from api.dependencies import require_student
from fastapi import Depends
from api.dependencies import exercise_controller

@router.get("/me/exercises")
def get_my_exercises(
    current_user=Depends(require_student)
):

    exercises = exercise_controller.get_exercises_by_level(
        current_user.level
    )

    return [
        {
            "exercise_id": exercise.exercise_id,
            "exercise_name": exercise.exercise_name,
            "course": {
                "course_id": exercise.course.course_id,
                "course_name": exercise.course.course_name,
                "semester": exercise.course.semester
            }
        }
        for exercise in exercises
    ]

from api.dependencies import require_student
from api.dependencies import submission_controller
from fastapi import Depends


@router.get("/me/submissions")
def get_my_submissions(
    current_user=Depends(require_student)
):

    submissions = submission_controller.get_submissions_by_student(
        current_user.student_id
    )

    return [
        {
            "submission_id": submission.submission_id,
            "student_id": submission.student_id,
            "exercise_id": submission.exercise.exercise_id,
            "submission_date": submission.submission_date,
            "file_path": submission.file_path,
            "status": submission.status
        }
        for submission in submissions
    ]

from api.schemas.submission_schema import (
    SubmissionCreate,
    SubmissionResponse
)

from api.dependencies import (
    require_student,
    submission_controller
)

from fastapi import Depends
@router.post("/me/submissions", response_model=SubmissionResponse)
def create_my_submission(
    data: SubmissionCreate,
    current_user=Depends(require_student)
):

    submission = submission_controller.create_submission(
        current_user.student_id,
        data.exercise_id,
        data.file_path
    )

    return {
        "submission_id": submission.submission_id,
        "student_id": submission.student_id,
        "exercise_id": submission.exercise.exercise_id,
        "submission_date": submission.submission_date,
        "file_path": submission.file_path,
        "status": submission.status
    }

from api.dependencies import require_student
from api.dependencies import grade_controller
from fastapi import Depends


@router.get("/me/grades")
def get_my_grades(
    current_user=Depends(require_student)
):

    grades = grade_controller.get_grades_by_student(
        current_user.student_id
    )

    return [
        {
            "grade_id": grade.grade_id,
            "score": grade.score,
            "exercise_id": grade.exercise.exercise_id
        }
        for grade in grades
    ]

from api.dependencies import notification_controller
from api.dependencies import require_student
from fastapi import Depends


@router.get("/me/notifications")
def get_my_notifications(
    current_user=Depends(require_student)
):

    notifications = notification_controller.get_student_notifications(
        current_user.student_id
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


@router.put("/me", response_model=StudentResponse)
def update_my_profile(
    data: StudentUpdate,
    current_user=Depends(require_student)
):
    updates = data.model_dump(exclude_none=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No data to update"
        )

    student_controller.update_student(
        current_user.student_id,
        **updates
    )

    updated_student = student_controller.get_student(
        current_user.student_id
    )

    return {
        "student_id": updated_student.student_id,
        "full_name": updated_student.full_name,
        "email": updated_student.email,
        "phone_number": updated_student.phone_number,
        "level": updated_student.level
    }

@router.get("/", response_model=list[StudentResponse])
def get_all_student():
    students = student_controller.get_all_students()
    return [{
        "student_id": student.student_id,
            "full_name": student.full_name,
            "email": student.email,
            "phone_number": student.phone_number,
            "level": student.level
    }
    for student in students]



from models.student import Student
from api.dependencies import student_controller

@router.post("/", response_model=StudentResponse)
def create_student(data: StudentCreate):

    result = student_controller.create_student(
        data.full_name,
        data.email,
        data.password,
        data.phone_number,
        data.level
    )

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Could not create student"
        )

    return {
        "student_id": result.student_id,
        "full_name": result.full_name,
        "email": result.email,
        "phone_number": result.phone_number,
        "level": result.level
    }

from api.schemas.student_schema import StudentUpdate

@router.put("/{student_id}")
def update_student(
    student_id: int,
    data: StudentUpdate
):
    student = student_controller.get_student(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    updates = data.model_dump(exclude_none=True)

    result = student_controller.update_student(
        student_id,
        **updates
    )

    return {
        "message": result
    }
# delete methode 
@router.delete("/{student_id}")
def delete_student(student_id: int):

    student = student_controller.get_student(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    result = student_controller.delete_student(student_id)

    return {
        "message": result
    }

@router.get("/search")
def search_students(full_name: str):

    students = student_controller.search_student(full_name)

    return [
        {
            "student_id": student.student_id,
            "full_name": student.full_name,
            "email": student.email,
            "phone_number": student.phone_number,
            "level": student.level
        }
        for student in students
    ]


@router.get("/count")
def count_students():

    count = student_controller.count_students()

    return {
        "count": count
    }

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    student = student_controller.get_student(student_id)
    if student is None:
        raise HTTPException(status_code=404,
                            detail = "Student not found")
    return {
        "student_id": student.student_id,
        "full_name": student.full_name,
        "email": student.email,
        "phone_number": student.phone_number,
        "level": student.level
    }

