from fastapi import APIRouter, HTTPException, Depends

from api.dependencies import (
    teacher_controller,
    require_teacher,
    course_controller,
    exercise_controller,
    student_controller
)

from api.schemas.teacher_schema import (
    TeacherResponse,
    TeacherCreate,
    TeacherUpdate
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

@router.get("/me/students")
def get_my_students(
    current_user=Depends(require_teacher)
):
    courses = course_controller.get_courses_by_teacher(current_user.teacher_id)

    levels = {course.level for course in courses}

    students = []
    for level in levels:
        students.extend(student_controller.get_students_by_level(level))

    unique_students = {}
    for student in students:
        unique_students[student.student_id] = student

    return [
        {
            "student_id": student.student_id,
            "full_name": student.full_name,
            "email": student.email,
            "phone_number": student.phone_number,
            "level": student.level
        }
        for student in unique_students.values()
    ]

from api.schemas.grade_schema import GradeCreate
from api.dependencies import grade_controller

# =========================================================
# MY GRADES
# =========================================================

from api.schemas.grade_schema import GradeCreate, GradeUpdate
from api.dependencies import grade_controller


@router.get("/me/grades")
def get_my_grades(
    current_user=Depends(require_teacher)
):

    grades = grade_controller.get_grades_by_teacher(
        current_user.teacher_id
    )

    return [
        {
            "grade_id": grade.grade_id,
            "score": grade.score,
            "student_id": grade.student.student_id,
            "exercise_id": grade.exercise.exercise_id
        }
        for grade in grades
    ]


@router.post("/me/grades")
def add_grade_to_student(
    data: GradeCreate,
    current_user=Depends(require_teacher)
):

    exercise = exercise_controller.get_exercise(
        data.exercise_id
    )

    if exercise is None:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    # Teacher can only grade his own exercise
    if exercise.course.teacher.teacher_id != current_user.teacher_id:
        raise HTTPException(
            status_code=403,
            detail="You can only grade your own exercises"
        )

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


@router.put("/me/grades/{grade_id}")
def update_my_grade(
    grade_id: int,
    data: GradeUpdate,
    current_user=Depends(require_teacher)
):

    try:

        result = grade_controller.update_grade_by_teacher(
            grade_id,
            current_user.teacher_id,
            data.score
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    
# =========================================================
# NOTIFICATIONS
# =========================================================

from api.schemas.notification_schema import NotificationCreate
from api.dependencies import notification_controller


@router.post("/me/notifications")
def send_notification_to_students(
    data: NotificationCreate,
    current_user=Depends(require_teacher)
):

    try:

        result = notification_controller.send_notification_to_students(
            current_user.teacher_id,
            data.title,
            data.message
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.post("/me/notifications/{student_id}")
def send_notification_to_student(
    student_id: int,
    data: NotificationCreate,
    current_user=Depends(require_teacher)
):

    try:

        result = notification_controller.send_notification_to_student(
            current_user.teacher_id,
            student_id,
            data.title,
            data.message
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