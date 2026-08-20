from fastapi import FastAPI
from api.routes.student_routes import router as student_router
from api.routes.teacher_router import router as teacher_router
from api.routes.course_router import router as course_router
from api.routes.exercise_router import router as exercise_router
from api.routes.notification_router import router as notification_router
from api.routes.student_notification_router import (
    router as student_notification_router
)
from api.routes.submission_router import router as submission_router
from api.routes.grade_router import router as grade_router

app = FastAPI(
    title = "EduAnalytics API",
    description="Backend API for EduAnalytics",
    version="1.0.0"
)

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(course_router)
app.include_router(exercise_router)
app.include_router(notification_router)
app.include_router(student_notification_router)
app.include_router(submission_router)
app.include_router(grade_router)

@app.get("/")
def root():
    return {
        "message": "EduAnalytics API is running"
    }

