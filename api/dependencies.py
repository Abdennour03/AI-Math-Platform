from database.database import Database

from repositories.student_repository import StudentRepo
from controllers.student_controller import StudentController

from repositories.teacher_repository import TeacherRepo
from controllers.teacher_controller import TeacherController

from repositories.course_repository import CourseRepo
from controllers.course_controller import CourseController

from repositories.exercise_repository import ExerciseRepo
from controllers.exercise_controller import ExerciseController

from controllers.notification_controller import NotificationController
from repositories.notification_repository import NotificationRepo
from repositories.student_notification_repository import StudentNotificationRepo

from repositories.submission_repository import SubmissionRepo
from controllers.submission_controller import SubmissionController

from repositories.grade_repository import GradeRepo
from controllers.grade_controller import GradeController

from controllers.auth_controller import AuthController
db = Database()

# Student
student_repo = StudentRepo(db)
student_controller = StudentController(student_repo)

# Teacher
teacher_repo = TeacherRepo(db)
teacher_controller = TeacherController(teacher_repo)

# Course
course_repo = CourseRepo(db)
course_controller = CourseController(
    course_repo,
    teacher_repo
)

exercise_repo = ExerciseRepo(db)
exercise_controller = ExerciseController(exercise_repo, course_repo)

notification_repo = NotificationRepo(db)

student_notification_repo = StudentNotificationRepo(
    db,
    student_repo,
    notification_repo
)

notification_controller = NotificationController(
    notification_repo,
    student_notification_repo,
    teacher_repo,
    student_repo
)

submission_repo = SubmissionRepo(
    db,
    student_repo,
    exercise_repo
)
submission_controller = SubmissionController(
    submission_repo,
    student_repo,
    exercise_repo
)

grade_repo = GradeRepo(db, student_repo, exercise_repo)

grade_controller = GradeController(
    grade_repo,
    student_repo,
    exercise_repo
)

auth_controller= AuthController(
    student_repo,
    teacher_repo
)

"""
create :
get_current_user()
require_student()
require_teacher()

"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from utils.security import decode_access_token
security = HTTPBearer()
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user_id = int(user_id)

        if role == "student":
            user = student_repo.get_student(user_id)

        elif role == "teacher":
            user = teacher_repo.get_teacher(user_id)

        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid role"
            )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def require_student(current_user=Depends(get_current_user)):

    if not hasattr(current_user, "student_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student access required"
        )

    return current_user


def require_teacher(current_user=Depends(get_current_user)):

    if not hasattr(current_user, "teacher_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher access required"
        )

    return current_user


