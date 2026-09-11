from models.course import Course


class CourseRepo:

    def __init__(self, db):
        self.db = db


    def add_course(self, course):

        self.db.cursor.execute("""
            INSERT INTO courses
            (course_name, teacher_id, semester, level)
            VALUES (?, ?, ?, ?)
        """, (
            course.course_name,
            course.teacher.teacher_id,
            course.semester,
            course.level
        ))

        self.db.connection.commit()

        course.course_id = self.db.cursor.lastrowid


    def get_course(self, course_id):

        self.db.cursor.execute("""
            SELECT course_id, course_name,
                   teacher_id, semester, level
            FROM courses
            WHERE course_id = ?
        """, (course_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        teacher_id = row[2]

        self.db.cursor.execute("""
            SELECT teacher_id, full_name, email,
                   password, phone_number
            FROM teachers
            WHERE teacher_id = ?
        """, (teacher_id,))

        teacher_row = self.db.cursor.fetchone()

        if teacher_row is None:
            return None

        from models.teacher import Teacher

        teacher = Teacher(
            teacher_row[0],
            teacher_row[1],
            teacher_row[2],
            teacher_row[4],
            teacher_row[3]
        )

        return Course(
            row[0],
            row[1],
            teacher,
            row[3],
            row[4]
        )


    def get_all_courses(self):

        self.db.cursor.execute("""
            SELECT
                courses.course_id,
                courses.course_name,
                courses.semester,
                courses.level,
                teachers.teacher_id,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM courses
            JOIN teachers
            ON courses.teacher_id = teachers.teacher_id
        """)

        rows = self.db.cursor.fetchall()

        courses = []

        from models.teacher import Teacher

        for row in rows:

            teacher = Teacher(
                row[4],  # teacher_id
                row[5],  # full_name
                row[6],  # email
                row[7],  # password
                row[8]   # phone_number
            )

            course = Course(
                row[0],  # course_id
                row[1],  # course_name
                teacher,
                row[2],  # level
                row[3]   # semester
            )

            courses.append(course)

        return courses


    def update_course(self, course_id, **kwargs):

        if "course_name" in kwargs:

            self.db.cursor.execute("""
                UPDATE courses
                SET course_name = ?
                WHERE course_id = ?
            """, (
                kwargs["course_name"],
                course_id
            ))


        if "teacher" in kwargs:

            self.db.cursor.execute("""
                UPDATE courses
                SET teacher_id = ?
                WHERE course_id = ?
            """, (
                kwargs["teacher"].teacher_id,
                course_id
            ))


        if "semester" in kwargs:

            self.db.cursor.execute("""
                UPDATE courses
                SET semester = ?
                WHERE course_id = ?
            """, (
                kwargs["semester"],
                course_id
            ))


        if "level" in kwargs:

            self.db.cursor.execute("""
                UPDATE courses
                SET level = ?
                WHERE course_id = ?
            """, (
                kwargs["level"],
                course_id
            ))


        self.db.connection.commit()

        return True


    def delete_course(self, course_id):

        course = self.get_course(course_id)

        if course is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM courses
            WHERE course_id = ?
        """, (course_id,))

        self.db.connection.commit()

        return True


    def search_course(self, query):

        self.db.cursor.execute("""
            SELECT course_id, course_name,
                   teacher_id, semester, level
            FROM courses
            WHERE course_name LIKE ?
        """, (f"%{query}%",))

        rows = self.db.cursor.fetchall()

        courses = []

        from models.teacher import Teacher

        for row in rows:

            self.db.cursor.execute("""
                SELECT teacher_id, full_name, email,
                       password, phone_number
                FROM teachers
                WHERE teacher_id = ?
            """, (row[2],))

            teacher_row = self.db.cursor.fetchone()

            if teacher_row is None:
                continue

            teacher = Teacher(
                teacher_row[0],
                teacher_row[1],
                teacher_row[2],
                teacher_row[3],
                teacher_row[4]
            )

            courses.append(
                Course(
                    row[0],
                    row[1],
                    teacher,
                    row[4],
                    row[3]
                )
            )

        return courses


    def count_courses(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM courses
        """)

        result = self.db.cursor.fetchone()

        return result[0]


    def get_courses_by_level(self, level):

        level = level.strip().upper()

        self.db.cursor.execute("""
            SELECT course_id, course_name, teacher_id, semester, level
            FROM courses
            WHERE UPPER(TRIM(level)) = ?
        """, (level,))

        matched_rows = self.db.cursor.fetchall()

        from models.teacher import Teacher

        courses = []

        for row in matched_rows:
            teacher_id = row[2]

            self.db.cursor.execute("""
                SELECT teacher_id, full_name, email, password, phone_number
                FROM teachers
                WHERE teacher_id = ?
            """, (teacher_id,))

            teacher_row = self.db.cursor.fetchone()

            if teacher_row is None:
                continue

            teacher = Teacher(
                teacher_row[0],
                teacher_row[1],
                teacher_row[2],
                teacher_row[3],
                teacher_row[4]
            )

            courses.append(
                Course(
                    row[0],        # course_id
                    row[1],        # course_name
                    teacher,
                    row[4],        # level
                    row[3]         # semester
                )
            )

        return courses

    def get_courses_by_class_id(self, class_id):
        self.db.cursor.execute(
            """SELECT courses.course_id
               FROM courses
               JOIN classes
                 ON UPPER(TRIM(courses.level)) = UPPER(TRIM(classes.name))
               WHERE classes.id = ?""",
            (class_id,),
        )
        return [
            course
            for (course_id,) in self.db.cursor.fetchall()
            if (course := self.get_course(course_id)) is not None
        ]

    def get_courses_by_teacher(self, teacher_id):

        self.db.cursor.execute("""
            SELECT
                courses.course_id,
                courses.course_name,
                courses.teacher_id,
                courses.semester,
                courses.level,
                teachers.teacher_id,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM courses
            JOIN teachers
                ON courses.teacher_id = teachers.teacher_id
            WHERE courses.teacher_id = ?
        """, (teacher_id,))

        rows = self.db.cursor.fetchall()

        courses = []

        from models.teacher import Teacher

        for row in rows:

            teacher = Teacher(
                row[5],
                row[6],
                row[7],
                row[8],
                row[9]
            )

            course = Course(
                row[0],
                row[1],
                teacher,
                row[4],
                row[3]
            )

            courses.append(course)

        return courses