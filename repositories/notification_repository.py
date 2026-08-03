class NotificationRepo:
    def __init__(self):
        self.notifications = []

    def add_notification(self, notification):
        self.notifications.append(notification)

    def get_notification(self, notification_id):
        for notification in self.notifications:
            if notification.notification_id == notification_id:
                return notification
        return None 


    def get_all_notifications(self):
        return self.notifications

    def update_notification(self, notification_id, **kwargs):
        for notification in self.notifications:
            if notification.notification_id == notification_id:
                for key, value in kwargs.items():
                    if hasattr(notification, key):
                        setattr(notification, key, value)
                return True 
        return False

    def delete_notification(self, notification_id):
        for index, notification in enumerate(self.notifications):
            if notification.notification_id == notification_id:
                del self.notifications[index]
                return True
        return False

    def search_notification(self, query):
        result_notifications = []
        for notification in self.notifications:
            if query.lower() in notification.notification_name.lower() :
                result_notifications.append(notification)
        return result_notifications


    def count_notifications(self):
        return len(self.notifications)