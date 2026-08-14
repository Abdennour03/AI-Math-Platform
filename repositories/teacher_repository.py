from models.teacher import Teacher


class TeacherRepo:

    def __init__(self, db):
        self.db = db

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                phone_number TEXT
            )
        """)

        self.db.connection.commit()


    def add_teacher(self, teacher):

        self.db.cursor.execute("""
            INSERT INTO teachers
            (full_name, email, password, phone_number)
            VALUES (?, ?, ?, ?)
        """, (
            teacher.full_name,
            teacher.email,
            teacher.password,
            teacher.phone_number
        ))

        self.db.connection.commit()

        teacher.teacher_id = self.db.cursor.lastrowid


    def get_teacher(self, teacher_id):

        self.db.cursor.execute("""
            SELECT teacher_id, full_name, email,
                   password, phone_number
            FROM teachers
            WHERE teacher_id = ?
        """, (teacher_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        return Teacher(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4]
        )


    def get_all_teachers(self):

        self.db.cursor.execute("""
            SELECT teacher_id, full_name, email,
                   password, phone_number
            FROM teachers
        """)

        rows = self.db.cursor.fetchall()

        teachers = []

        for row in rows:
            teacher = Teacher(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            )

            teachers.append(teacher)

        return teachers


    def update_teacher(self, teacher_id, **kwargs):

        if "full_name" in kwargs:

            self.db.cursor.execute("""
                UPDATE teachers
                SET full_name = ?
                WHERE teacher_id = ?
            """, (kwargs["full_name"], teacher_id))


        if "email" in kwargs:

            self.db.cursor.execute("""
                UPDATE teachers
                SET email = ?
                WHERE teacher_id = ?
            """, (kwargs["email"], teacher_id))


        if "password" in kwargs:

            self.db.cursor.execute("""
                UPDATE teachers
                SET password = ?
                WHERE teacher_id = ?
            """, (kwargs["password"], teacher_id))


        if "phone_number" in kwargs:

            self.db.cursor.execute("""
                UPDATE teachers
                SET phone_number = ?
                WHERE teacher_id = ?
            """, (kwargs["phone_number"], teacher_id))


        self.db.connection.commit()

        return True


    def delete_teacher(self, teacher_id):

        teacher = self.get_teacher(teacher_id)

        if teacher is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM teachers
            WHERE teacher_id = ?
        """, (teacher_id,))

        self.db.connection.commit()

        return True


    def search_teacher(self, full_name):

        self.db.cursor.execute("""
            SELECT teacher_id, full_name, email,
                   password, phone_number
            FROM teachers
            WHERE full_name LIKE ?
        """, (f"%{full_name}%",))

        rows = self.db.cursor.fetchall()

        teachers = []

        for row in rows:
            teacher = Teacher(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            )

            teachers.append(teacher)

        return teachers


    def count_teacher(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM teachers
        """)

        result = self.db.cursor.fetchone()

        return result[0]