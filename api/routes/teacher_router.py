from fastapi import APIRouter, HTTPException, Depends

from api.schemas.teacher_schema import (
    TeacherResponse,
    TeacherCreate,
    TeacherUpdate
)

from api.dependencies import teacher_controller

from api.schemas.teacher_schema import (
    TeacherResponse,
    TeacherCreate,
    TeacherUpdate
)

from api.dependencies import (
    teacher_controller,
    require_teacher,
    course_controller,
    exercise_controller
)
router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)

@router.get("/me", response_model=TeacherResponse)
def get_my_profile(
    current_user=Depends(require_teacher)
):

    return {
        "teacher_id": current_user.teacher_id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone_number": current_user.phone_number
    }


@router.put("/me")
def update_my_profile(
    data: TeacherUpdate,
    current_user=Depends(require_teacher)
):

    updates = data.model_dump(exclude_none=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No data to update"
        )

    result = teacher_controller.update_teacher(
        current_user.teacher_id,
        **updates
    )

    return {
        "message": result
    }


# =========================================================
# MY COURSES
# =========================================================

@router.get("/me/courses")
def get_my_courses(
    current_user=Depends(require_teacher)
):

    courses = course_controller.get_courses_by_teacher(
        current_user.teacher_id
    )

    return [
        {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "semester": course.semester,
            "level": course.level
        }
        for course in courses
    ]

# =========================================================
# MY EXERCISES
# =========================================================

@router.get("/me/exercises")
def get_my_exercises(
    current_user=Depends(require_teacher)
):

    exercises = exercise_controller.get_exercises_by_teacher(
        current_user.teacher_id
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

from api.schemas.course_schema import CourseCreate

@router.post("/me/courses")
def create_my_course(
    data: CourseCreate,
    current_user=Depends(require_teacher)
):
    try:
        result = course_controller.create_course(
            data.course_name,
            current_user.teacher_id,
            data.level,
            data.semester
        )

        return {
            "message": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


from api.schemas.exercise_schema import ExerciseCreate

@router.post("/me/exercises")
def create_my_exercise(
    data: ExerciseCreate,
    current_user=Depends(require_teacher)
):

    try:

        result = exercise_controller.create_exercise(
            data.exercise_name,
            data.course_id,
            current_user.teacher_id
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )    
@router.get("/", response_model=list[TeacherResponse])
def get_all_teachers():

    teachers = teacher_controller.get_all_teachers()

    return [
        {
            "teacher_id": teacher.teacher_id,
            "full_name": teacher.full_name,
            "email": teacher.email,
            "phone_number": teacher.phone_number
        }
        for teacher in teachers
    ]


@router.post("/")
def create_teacher(data: TeacherCreate):

    result = teacher_controller.create_teacher(
        data.full_name,
        data.email,
        data.password,
        data.phone_number
    )

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Could not create teacher"
        )

    return {
        "message": result
    }


@router.get("/search")
def search_teachers(full_name: str):

    teachers = teacher_controller.search_teacher(full_name)

    return [
        {
            "teacher_id": teacher.teacher_id,
            "full_name": teacher.full_name,
            "email": teacher.email,
            "phone_number": teacher.phone_number
        }
        for teacher in teachers
    ]


@router.get("/count")
def count_teachers():

    count = teacher_controller.count_teachers()

    return {
        "count": count
    }


@router.put("/{teacher_id}")
def update_teacher(
    teacher_id: int,
    data: TeacherUpdate
):

    teacher = teacher_controller.get_teacher(teacher_id)

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    updates = data.model_dump(exclude_none=True)

    result = teacher_controller.update_teacher(
        teacher_id,
        **updates
    )

    return {
        "message": result
    }


@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int):

    teacher = teacher_controller.get_teacher(teacher_id)

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    result = teacher_controller.delete_teacher(teacher_id)

    return {
        "message": result
    }


@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(teacher_id: int):

    teacher = teacher_controller.get_teacher(teacher_id)

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return {
        "teacher_id": teacher.teacher_id,
        "full_name": teacher.full_name,
        "email": teacher.email,
        "phone_number": teacher.phone_number
    }