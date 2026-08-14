from models.notification import Notification
from models.teacher import Teacher


class NotificationRepo:

    def __init__(self, db):
        self.db = db

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                sender_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (sender_id)
                    REFERENCES teachers(teacher_id)
            )
        """)

        self.db.connection.commit()


    def add_notification(self, notification):

        self.db.cursor.execute("""
            INSERT INTO notifications
            (title, message, sender_id, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            notification.title,
            notification.message,
            notification.sender.teacher_id,
            notification.created_at
        ))

        self.db.connection.commit()

        notification.notification_id = self.db.cursor.lastrowid


    def get_notification(self, notification_id):

        self.db.cursor.execute("""
            SELECT
                notifications.notification_id,
                notifications.title,
                notifications.message,
                notifications.sender_id,
                notifications.created_at,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM notifications

            JOIN teachers
                ON notifications.sender_id = teachers.teacher_id

            WHERE notifications.notification_id = ?
        """, (notification_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        teacher = Teacher(
            row[3],
            row[5],
            row[6],
            row[7],
            row[8]
        )

        return Notification(
            row[0],
            row[1],
            row[2],
            teacher,
            row[4]
        )


    def get_all_notifications(self):

        self.db.cursor.execute("""
            SELECT
                notifications.notification_id,
                notifications.title,
                notifications.message,
                notifications.sender_id,
                notifications.created_at,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM notifications

            JOIN teachers
                ON notifications.sender_id = teachers.teacher_id
        """)

        rows = self.db.cursor.fetchall()

        notifications = []

        for row in rows:

            teacher = Teacher(
                row[3],
                row[5],
                row[6],
                row[7],
                row[8]
            )

            notification = Notification(
                row[0],
                row[1],
                row[2],
                teacher,
                row[4]
            )

            notifications.append(notification)

        return notifications


    def update_notification(self, notification_id, **kwargs):

        if "title" in kwargs:

            self.db.cursor.execute("""
                UPDATE notifications
                SET title = ?
                WHERE notification_id = ?
            """, (
                kwargs["title"],
                notification_id
            ))


        if "message" in kwargs:

            self.db.cursor.execute("""
                UPDATE notifications
                SET message = ?
                WHERE notification_id = ?
            """, (
                kwargs["message"],
                notification_id
            ))


        if "sender" in kwargs:

            self.db.cursor.execute("""
                UPDATE notifications
                SET sender_id = ?
                WHERE notification_id = ?
            """, (
                kwargs["sender"].teacher_id,
                notification_id
            ))


        if "created_at" in kwargs:

            self.db.cursor.execute("""
                UPDATE notifications
                SET created_at = ?
                WHERE notification_id = ?
            """, (
                kwargs["created_at"],
                notification_id
            ))


        self.db.connection.commit()

        return True


    def delete_notification(self, notification_id):

        notification = self.get_notification(notification_id)

        if notification is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM notifications
            WHERE notification_id = ?
        """, (notification_id,))

        self.db.connection.commit()

        return True


    def search_notification(self, query):

        self.db.cursor.execute("""
            SELECT
                notifications.notification_id,
                notifications.title,
                notifications.message,
                notifications.sender_id,
                notifications.created_at,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM notifications

            JOIN teachers
                ON notifications.sender_id = teachers.teacher_id

            WHERE notifications.title LIKE ?
               OR notifications.message LIKE ?
        """, (
            f"%{query}%",
            f"%{query}%"
        ))

        rows = self.db.cursor.fetchall()

        notifications = []

        for row in rows:

            teacher = Teacher(
                row[3],
                row[5],
                row[6],
                row[7],
                row[8]
            )

            notification = Notification(
                row[0],
                row[1],
                row[2],
                teacher,
                row[4]
            )

            notifications.append(notification)

        return notifications


    def count_notifications(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM notifications
        """)

        result = self.db.cursor.fetchone()

        return result[0]