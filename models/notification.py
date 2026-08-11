class Notification:
    def __init__(self, notification_id, title, message, sender, receiver, created_at=None):
            self.notification_id = notification_id
            self.title = title
            self.message = message
            self.sender = sender
            self.receiver = receiver
            self.created_at = created_at