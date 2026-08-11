class StudentNotificationRepo:
    def __init__(self):
        self.student_notifications = []
        self.next_id = 1

    def add_student_notification(self, student_notification):

        student_notification.student_notification_id = self.next_id
        self.next_id += 1

        self.student_notifications.append(
            student_notification
        )

    def get_student_notification(self, student_notification_id):

        for item in self.student_notifications:

            if item.student_notification_id == student_notification_id:
                return item

        return None

    def get_all_student_notifications(self):

        return self.student_notifications

    def get_notifications_for_student(self, student_id):

        return [
            item
            for item in self.student_notifications
            if item.student.student_id == student_id
        ]

    def mark_as_read(self, student_notification_id):

        student_notification = self.get_student_notification(
            student_notification_id
        )

        if student_notification is None:
            return False

        student_notification.is_read = True

        return True

    def delete_student_notification(self, student_notification_id):

        for index, item in enumerate(self.student_notifications):

            if item.student_notification_id == student_notification_id:

                del self.student_notifications[index]

                return True

        return False

    def count_student_notifications(self):

        return len(self.student_notifications)