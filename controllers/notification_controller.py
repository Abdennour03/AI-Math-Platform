from utils.notification_validation import NotificationValidator
from models.notification import Notification



class NotificationController:
    def __init__(self, notification_repo):
        self.notification_repo = notification_repo

    def create_notification(self, title, message, receiver, created_at):

        NotificationValidator.validation_title(title)
        NotificationValidator.validation_message(message)

        notification = Notification(None, title, message, receiver, created_at)
        self.notification_repo.add_notification(notification)
        return "notification created successfullty."


    
    def get_notification(self, notification_id):
        if not isinstance(notification_id, int):
            raise ValueError("notification ID mustbe int.")
        notification = self.notification_repo.get_notification(notification_id)
        if notification is None:
            raise ValueError("notification not found")
        return notification

    
    def get_all_notifications(self):
        return self.notification_repo.get_all_notifications()

    def update_notification(self, notification_id, **kwargs):

        notification = self.notification_repo.get_notification(notification_id)
        if notification is None:
            raise ValueError("notification not found.")
        if "title" in kwargs:
            NotificationValidator.validation_title(kwargs["title"])
        if "message" in kwargs:
            NotificationValidator.validation_message(kwargs["message"])

        self.notification_repo.update_notification(notification_id, **kwargs)
        return "notification updated successfully"
    
    def delete_notification(self, notification_id):
        if not isinstance(notification_id, int):
            raise ValueError("notification ID must be int")
        notification = self.notification_repo.get_notification(notification_id)
        if notification is None:
            raise ValueError("notification not found.")
        self.notification_repo.delete_notification(notification_id)
        return "notification deleted succssefully."

    def search_notification(self, query):
        query = query.strip()

        if not query:
            raise ValueError("Search query cannot be empty.")
        
        notifications = self.notification_repo.search_notification(query)
        if not notifications :
            raise ValueError(" No notification found.")
        return notifications


    def count_notifications(self):
        return self.notification_repo.count_notifications()