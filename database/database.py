import sqlite3


class Database:
    def __init__(self, db_name="eduinsight.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        existing_classes = self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'classes'"
        ).fetchone()
        if existing_classes:
            existing_class_columns = {
                row[1] for row in self.cursor.execute("PRAGMA table_info(classes)")
            }
            if "id" not in existing_class_columns:
                self.cursor.execute("ALTER TABLE classes ADD COLUMN id INTEGER")
                if "class_id" in existing_class_columns:
                    self.cursor.execute(
                        "UPDATE classes SET id = class_id WHERE id IS NULL"
                    )
            self.cursor.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_classes_canonical_id ON classes(id)"
            )
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                academic_year TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                phone_number TEXT,
                level TEXT NOT NULL,
                class_id INTEGER,
                FOREIGN KEY (class_id) REFERENCES classes(id)
            );
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                phone_number TEXT,
                class_id INTEGER,
                FOREIGN KEY (class_id) REFERENCES classes(id)
            );
            CREATE TABLE IF NOT EXISTS teacher_classes (
                teacher_id INTEGER NOT NULL,
                class_id INTEGER NOT NULL,
                PRIMARY KEY (teacher_id, class_id),
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                teacher_id INTEGER NOT NULL,
                semester TEXT NOT NULL,
                level TEXT NOT NULL,
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
            );
            CREATE TABLE IF NOT EXISTS exercises (
                exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_name TEXT NOT NULL,
                course_id INTEGER NOT NULL,
                max_score REAL NOT NULL DEFAULT 20,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            );
            CREATE TABLE IF NOT EXISTS submissions (
                submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                submission_date TEXT NOT NULL,
                file_path TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
            );
            CREATE TABLE IF NOT EXISTS grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                score REAL NOT NULL,
                student_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id),
                UNIQUE (student_id, exercise_id)
            );
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                sender_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (sender_id) REFERENCES teachers(teacher_id)
            );
            CREATE TABLE IF NOT EXISTS student_notifications (
                student_notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                notification_id INTEGER NOT NULL,
                is_read INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (notification_id) REFERENCES notifications(notification_id)
            );
            """
        )
        exercise_columns = {
            row[1]
            for row in self.cursor.execute("PRAGMA table_info(exercises)")
        }
        if "max_score" not in exercise_columns:
            self.cursor.execute(
                "ALTER TABLE exercises ADD COLUMN max_score REAL NOT NULL DEFAULT 20"
            )
        student_columns = {
            row[1] for row in self.cursor.execute("PRAGMA table_info(students)")
        }
        if "class_id" not in student_columns:
            self.cursor.execute(
                "ALTER TABLE students ADD COLUMN class_id INTEGER REFERENCES classes(class_id)"
            )
        teacher_columns = {
            row[1] for row in self.cursor.execute("PRAGMA table_info(teachers)")
        }
        if "class_id" not in teacher_columns:
            self.cursor.execute(
                "ALTER TABLE teachers ADD COLUMN class_id INTEGER REFERENCES classes(id)"
            )
        admin_columns = {
            row[1] for row in self.cursor.execute("PRAGMA table_info(admins)")
        }
        if "id" not in admin_columns:
            self.cursor.execute("ALTER TABLE admins ADD COLUMN id INTEGER")
        if "password_hash" not in admin_columns:
            self.cursor.execute("ALTER TABLE admins ADD COLUMN password_hash TEXT")
        if "created_at" not in admin_columns:
            self.cursor.execute("ALTER TABLE admins ADD COLUMN created_at TEXT")
        class_columns = {
            row[1] for row in self.cursor.execute("PRAGMA table_info(classes)")
        }
        if "id" not in class_columns:
            self.cursor.execute("ALTER TABLE classes ADD COLUMN id INTEGER")
            if "class_id" in class_columns:
                self.cursor.execute(
                    "UPDATE classes SET id = class_id WHERE id IS NULL"
                )
        self.cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_classes_canonical_id ON classes(id)"
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS teacher_classes (
                teacher_id INTEGER NOT NULL,
                class_id INTEGER NOT NULL,
                PRIMARY KEY (teacher_id, class_id),
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
            )"""
        )
        self.cursor.execute(
            """INSERT OR IGNORE INTO teacher_classes (teacher_id, class_id)
               SELECT teacher_id, class_id FROM teachers
               WHERE class_id IS NOT NULL"""
        )
        if "admin_id" in admin_columns and "password" in admin_columns:
            self.cursor.execute(
                """UPDATE admins
                   SET id = COALESCE(id, admin_id),
                       password_hash = COALESCE(password_hash, password),
                       created_at = COALESCE(created_at, CURRENT_TIMESTAMP)
                   WHERE id IS NULL OR password_hash IS NULL OR created_at IS NULL"""
            )
        self.cursor.execute(
            "SELECT 1 FROM admins WHERE email = ? LIMIT 1",
            ("admin@eduinsight.ai",),
        )
        if self.cursor.fetchone() is None:
            from utils.security import hash_password

            password_hash = hash_password("adminpassword")
            admin_id = self.cursor.execute(
                "SELECT COALESCE(MAX(id), 0) + 1 FROM admins"
            ).fetchone()[0]
            if "password" in admin_columns:
                self.cursor.execute(
                    """INSERT INTO admins
                       (id, email, password, password_hash, full_name, created_at)
                       VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                    (
                        admin_id,
                        "admin@eduinsight.ai",
                        password_hash,
                        password_hash,
                        "EduInsight Administrator",
                    ),
                )
            else:
                self.cursor.execute(
                          """INSERT INTO admins (id, email, password_hash, full_name)
                              VALUES (?, ?, ?, ?)""",
                    (
                                admin_id,
                        "admin@eduinsight.ai",
                        password_hash,
                        "EduInsight Administrator",
                    ),
                )
        self.connection.commit()

    def close(self):
        self.connection.close()
