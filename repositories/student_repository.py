from models.student import Student

class StudentRepo:
    def __init__(self, db):
        self.db = db
        
    def add_student(self, student):
        self.db.cursor.execute("""
    INSERT INTO students
    (full_name, email, password, phone_number, level)
    VALUES (?, ?, ?, ?, ?)
        """,
        (student.full_name,
         student.email,
         student.password,
         student.phone_number,
         student.level
         ))
        self.db.connection.commit()
        student.student_id = self.db.cursor.lastrowid



    def get_student(self, student_id):
        self.db.cursor.execute("""
        SELECT student_id, full_name, email,
               password, phone_number, level
        FROM students
        WHERE student_id = ?
    """, (student_id,))

        row = self.db.cursor.fetchone()
        if row is None:
            return None

        return Student(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        )
    def get_all_student(self):
        self.db.cursor.execute("""
        SELECT student_id, full_name, email,
               password, phone_number, level
        FROM students
    """)

        rows = self.db.cursor.fetchall()

        students = []

        for row in rows:
            students.append(
                Student(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )
            )

        return students

    def get_students_by_level(self, level):
        self.db.cursor.execute("""
            SELECT student_id, full_name, email,
                   password, phone_number, level
            FROM students
            WHERE UPPER(TRIM(level)) = ?
        """, (level.strip().upper(),))

        rows = self.db.cursor.fetchall()
        students = []

        for row in rows:
            students.append(
                Student(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )
            )

        return students
        
    def update_student(self, student_id, **kwargs):
        student = self.get_student(student_id)
        if not kwargs:
            return False
        if "full_name" in kwargs:
            self.db.cursor.execute("""
        UPDATE students
            SET full_name = ?
            WHERE student_id = ?
            """, (kwargs["full_name"], student_id))


        if "email" in kwargs:
            self.db.cursor.execute("""
        UPDATE students
            SET email = ?
            WHERE student_id = ?
            """, (kwargs["email"], student_id))


        if "password" in kwargs:
                self.db.cursor.execute("""
        UPDATE students
            SET password = ?
            WHERE student_id = ?
            """, (kwargs["password"], student_id))


        if "phone_number" in kwargs:
                self.db.cursor.execute("""
        UPDATE students
            SET phone_number = ?
            WHERE student_id = ?
            """, (kwargs["phone_number"], student_id))


        if "level" in kwargs:
                self.db.cursor.execute("""
        UPDATE students
            SET level = ?
            WHERE student_id = ?
            """, (kwargs["level"], student_id))

        self.db.connection.commit() 
                

    def delete_student(self, student_id):
        student = self.get_student(student_id)
        if student is None:
             return False
        self.db.cursor.execute("""
DELETE FROM students
WHERE student_id = ?""", (student_id,))
        self.db.connection.commit()
        return True

    
    def search_student(self, name):

        self.db.cursor.execute("""
            SELECT student_id, full_name, email,
                password, phone_number, level
            FROM students
            WHERE full_name LIKE ?
        """, (f"%{name}%",))

        rows = self.db.cursor.fetchall()
        students = []

        for row in rows:
            students.append(
                Student(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )
            )

        return students

    
    def count_students(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM students
        """)
        result = self.db.cursor.fetchone()

        return result[0]

    def get_student_by_email(self, email):

        self.db.cursor.execute("""
            SELECT
                student_id,
                full_name,
                email,
                password,
                phone_number,
                level
            FROM students
            WHERE email = ?
        """, (email,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        return Student(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        )
    def get_students_by_level(self, level):
        self.db.cursor.execute("""
            SELECT student_id, full_name, email, password, phone_number, level
            FROM students
            WHERE UPPER(TRIM(level)) = ?
        """, (level.strip().upper(),))

        rows = self.db.cursor.fetchall()
        students = []

        for row in rows:
            students.append(
                Student(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )
            )

        return students