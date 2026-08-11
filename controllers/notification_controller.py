from utils.notification_validation import NotificationValidator
from models.notification import Notification
from models.teacher import Teacher
from models.student import Student
from datetime import datetime
from models.student_notification import StudentNotification




class NotificationController:
    def __init__(self, notification_repo,student_notification_repo ,teacher_repo, student_repo):
        self.notification_repo = notification_repo
        self.student_notification_repo = student_notification_repo
        self.teacher_repo = teacher_repo
        self.student_repo = student_repo

    def create_notification(self, title, message, teacher_id):

        NotificationValidator.validation_title(title)
        NotificationValidator.validation_message(message)

        created_at = datetime.now()
        teacher = self.teacher_repo.get_teacher(teacher_id)
        if not isinstance(teacher_id, int):
            raise ValueError("Teacher ID must be an integer.")
        if teacher is None:
            raise ValueError("Teacher not found.")
    
        notification = Notification(None, title, message, teacher, created_at)
        self.notification_repo.add_notification(notification)
        return notification

    
    def send_to_all_students(self, notification):

        students = self.student_repo.get_all_student()
        if not students:
            raise ValueError("No students found.")

        for student in students:
            student_notification = StudentNotification(
                None,
                student,
                notification
            )
            self.student_notification_repo.add_student_notification(
                student_notification
            )

        return "Notification sent to all students."

    def send_to_student(self, notification, student_id):
        if not isinstance(student_id, int):
            raise ValueError("Student ID must be an integer.")
        student = self.student_repo.get_student(student_id)
        if student is None:
            raise ValueError("Student not found.")
        student_notification = StudentNotification(None, student, notification)
        self.student_notification_repo.add_student_notification(student_notification)
        return "Notification sent to student."


    def get_notification(self, notification_id):

        if not isinstance(notification_id, int):
            raise ValueError("notification ID mustbe int.")
        notification = self.notification_repo.get_notification(notification_id)
        if notification is None:
            raise ValueError("notification not found")
        return notification

    
    def get_all_notifications(self):
        return self.notification_repo.get_all_notifications()

    def get_student_notifications(self, student_id):

        if not isinstance(student_id, int):
            raise ValueError(
                "Student ID must be an integer."
            )

        student = self.student_repo.get_student(student_id)
        if student is None:
            raise ValueError(
                "Student not found."
            )

        return self.student_notification_repo.get_notifications_for_student(
            student_id
        )

    def mark_as_read(self, student_notification_id):

        if not isinstance(student_notification_id, int):
            raise ValueError(
                "Student Notification ID must be an integer."
            )
        result = self.student_notification_repo.mark_as_read(
            student_notification_id
        )
        if not result:
            raise ValueError(
                "Student notification not found."
            )
        return "Notification marked as read."

    
    def delete_notification(self, notification_id):
        if not isinstance(notification_id, int):
            raise ValueError("notification ID must be int")
        notification = self.notification_repo.get_notification(notification_id)
        if notification is None:
            raise ValueError("notification not found.")
        self.notification_repo.delete_notification(notification_id)
        return "notification deleted succssefully."

