from fastapi import APIRouter, HTTPException

from api.schemas.exercise_schema import (
    ExerciseResponse,
    ExerciseCreate,
    ExerciseUpdate
)

from api.dependencies import exercise_controller


router = APIRouter(
    prefix="/exercises",
    tags=["exercises"]
)


@router.get("/", response_model=list[ExerciseResponse])
def get_all_exercises():

    exercises = exercise_controller.get_all_exercises()

    return [
        {
            "exercise_id": exercise.exercise_id,
            "exercise_name": exercise.exercise_name,
            "course_id": exercise.course.course_id,
        }
        for exercise in exercises
    ]


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int):

    try:
        exercise = exercise_controller.get_exercise(exercise_id)

        return {
            "exercise_id": exercise.exercise_id,
            "exercise_name": exercise.exercise_name,
            "course_id": exercise.course.course_id,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/")
def create_exercise(data: ExerciseCreate):

    try:

        result = exercise_controller.create_exercise(
            data.exercise_name,
            data.course_id,
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/{exercise_id}")
def update_exercise(
    exercise_id: int,
    data: ExerciseUpdate
):

    try:

        updates = data.model_dump(exclude_none=True)

        result = exercise_controller.update_exercise(
            exercise_id,
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


@router.delete("/{exercise_id}")
def delete_exercise(exercise_id: int):

    try:

        result = exercise_controller.delete_exercise(
            exercise_id
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get("/search")
def search_exercises(query: str):

    try:

        exercises = exercise_controller.search_exercise(query)

        return [
            {
                "exercise_id": exercise.exercise_id,
                "exercise_name": exercise.exercise_name,
                "course_id": exercise.course.course_id,
            }
            for exercise in exercises
        ]

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get("/count")
def count_exercises():

    return {
        "count": exercise_controller.count_exercise()
    }