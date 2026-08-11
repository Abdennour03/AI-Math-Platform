class StudentNotification:
    def __init__(self, student_notification_id, student, notification, is_read=False):
        self.student_notification_id = student_notification_id
        self.student = student
        self.notification = notification
        self.is_read = is_read