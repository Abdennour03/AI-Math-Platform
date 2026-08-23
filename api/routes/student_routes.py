from fastapi import APIRouter
from api.schemas.student_schema import (StudentResponse , StudentCreate)
from api.dependencies import student_controller
from fastapi import APIRouter , HTTPException
router = APIRouter(
    prefix="/students",
    tags = ["Students"]
)


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