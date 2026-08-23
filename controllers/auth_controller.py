from utils.security import (
    verify_password,
    create_access_token
)


class AuthController:

    def __init__(self, student_repo, teacher_repo):
        self.student_repo = student_repo
        self.teacher_repo = teacher_repo

    def login(self, email, password):

        student = self.student_repo.get_student_by_email(email)

        if student is not None:

            if verify_password(
                password,
                student.password
            ):

                token = create_access_token({
                    "sub": str(student.student_id),
                    "role": "student"
                })

                return {
                    "access_token": token,
                    "token_type": "bearer",
                    "role": "student"
                }

        teacher = self.teacher_repo.get_teacher_by_email(email)

        if teacher is not None:

            if verify_password(
                password,
                teacher.password
            ):

                token = create_access_token({
                    "sub": str(teacher.teacher_id),
                    "role": "teacher"
                })

                return {
                    "access_token": token,
                    "token_type": "bearer",
                    "role": "teacher"
                }

        return None