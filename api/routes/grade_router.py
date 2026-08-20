from fastapi import APIRouter, HTTPException

from api.schemas.grade_schema import (
    GradeCreate,
    GradeUpdate,
    GradeResponse
)

from api.dependencies import grade_controller


router = APIRouter(
    prefix="/grades",
    tags=["grades"]
)


def grade_to_response(grade):

    return {
        "grade_id": grade.grade_id,
        "score": grade.score,
        "student_id": grade.student.student_id,
        "exercise_id": grade.exercise.exercise_id
    }


@router.post(
    "/",
    response_model=dict
)
def create_grade(data: GradeCreate):

    try:

        result = grade_controller.create_grade(
            data.score,
            data.student_id,
            data.exercise_id
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get(
    "/",
    response_model=list[GradeResponse]
)
def get_all_grades():

    grades = grade_controller.get_all_grades()

    return [
        grade_to_response(grade)
        for grade in grades
    ]


@router.get(
    "/student/{student_id}",
    response_model=list[GradeResponse]
)
def get_grades_by_student(student_id: int):

    try:

        grades = (
            grade_controller
            .search_grade_by_student(student_id)
        )

        return [
            grade_to_response(grade)
            for grade in grades
        ]

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get(
    "/exercise/{exercise_id}",
    response_model=list[GradeResponse]
)
def get_grades_by_exercise(exercise_id: int):

    try:

        grades = (
            grade_controller
            .search_grade_by_exercise(exercise_id)
        )

        return [
            grade_to_response(grade)
            for grade in grades
        ]

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@router.get(
    "/count",
    response_model=dict
)
def count_grades():

    return {
        "count": grade_controller.count_grades()
    }

@router.get(
    "/{grade_id}",
    response_model=GradeResponse
)
def get_grade(grade_id: int):

    try:

        grade = grade_controller.get_grade(
            grade_id
        )

        return grade_to_response(grade)

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put(
    "/{grade_id}",
    response_model=dict
)
def update_grade(
    grade_id: int,
    data: GradeUpdate
):

    try:

        updates = data.model_dump(
            exclude_none=True
        )

        result = grade_controller.update_grade(
            grade_id,
            **updates
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.delete(
    "/{grade_id}",
    response_model=dict
)
def delete_grade(grade_id: int):

    try:

        result = grade_controller.delete_grade(
            grade_id
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )