class NotificationValidator:
    @staticmethod
    def validation_title(title):
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        if len(title) < 5:
            raise ValueError("Title must contain at least 5 characters.")
        if len(title) > 100:
            raise ValueError("Title must contain at exceed 100 characters.")

        @staticmethod
        def validation_message(message):
            message = message.strip()
            if not message:
                raise ValueError("Message cannot be empty.")

            if len(message) > 1000:
                raise ValueError("Message is too long.")