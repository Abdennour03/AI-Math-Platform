from models.exercise import Exercise
from models.course import Course
from models.teacher import Teacher


class ExerciseRepo:

    def __init__(self, db):
        self.db = db

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
                exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_name TEXT NOT NULL,
                course_id INTEGER NOT NULL,
                FOREIGN KEY (course_id)
                    REFERENCES courses(course_id)
)
        """)

        self.db.connection.commit()


    def add_exercise(self, exercise):

        self.db.cursor.execute("""
            INSERT INTO exercises
            (exercise_name, course_id, level)
            VALUES (?, ?, ?)
        """, (
            exercise.exercise_name,
            exercise.course.course_id,
            exercise.level
        ))

        self.db.connection.commit()

        exercise.exercise_id = self.db.cursor.lastrowid


    def get_exercise(self, exercise_id):

        self.db.cursor.execute("""
            SELECT
                exercise_id,
                exercise_name,
                course_id,
                level
            FROM exercises
            WHERE exercise_id = ?
        """, (exercise_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        course_id = row[2]

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
            WHERE courses.course_id = ?
        """, (course_id,))

        course_row = self.db.cursor.fetchone()

        if course_row is None:
            return None

        teacher = Teacher(
            course_row[5],
            course_row[6],
            course_row[7],
            course_row[8],
            course_row[9]
        )

        course = Course(
            course_row[0],
            course_row[1],
            teacher,
            course_row[3],
            course_row[4]
        )

        return Exercise(
            row[0],
            row[1],
            course,
        )


    def get_all_exercises(self):

        self.db.cursor.execute("""
            SELECT
                exercises.exercise_id,
                exercises.exercise_name,
                exercises.level,
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
            FROM exercises

            JOIN courses
                ON exercises.course_id = courses.course_id

            JOIN teachers
                ON courses.teacher_id = teachers.teacher_id
        """)

        rows = self.db.cursor.fetchall()

        exercises = []

        for row in rows:

            teacher = Teacher(
                row[8],
                row[9],
                row[10],
                row[11],
                row[12]
            )

            course = Course(
                row[3],
                row[4],
                teacher,
                row[6],
                row[7]
            )

            exercise = Exercise(
                row[0],
                row[1],
                course,
            )

            exercises.append(exercise)

        return exercises


    def update_exercise(self, exercise_id, **kwargs):

        if "exercise_name" in kwargs:

            self.db.cursor.execute("""
                UPDATE exercises
                SET exercise_name = ?
                WHERE exercise_id = ?
            """, (
                kwargs["exercise_name"],
                exercise_id
            ))


        if "course" in kwargs:

            self.db.cursor.execute("""
                UPDATE exercises
                SET course_id = ?
                WHERE exercise_id = ?
            """, (
                kwargs["course"].course_id,
                exercise_id
            ))


        if "level" in kwargs:

            self.db.cursor.execute("""
                UPDATE exercises
                SET level = ?
                WHERE exercise_id = ?
            """, (
                kwargs["level"],
                exercise_id
            ))


        self.db.connection.commit()

        return True


    def delete_exercise(self, exercise_id):

        exercise = self.get_exercise(exercise_id)

        if exercise is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM exercises
            WHERE exercise_id = ?
        """, (exercise_id,))

        self.db.connection.commit()

        return True


    def search_exercise(self, query):

        self.db.cursor.execute("""
            SELECT
                exercises.exercise_id,
                exercises.exercise_name,
                exercises.level,
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
            FROM exercises

            JOIN courses
                ON exercises.course_id = courses.course_id

            JOIN teachers
                ON courses.teacher_id = teachers.teacher_id

            WHERE exercises.exercise_name LIKE ?
        """, (f"%{query}%",))

        rows = self.db.cursor.fetchall()

        exercises = []

        for row in rows:

            teacher = Teacher(
                row[8],
                row[9],
                row[10],
                row[11],
                row[12]
            )

            course = Course(
                row[3],
                row[4],
                teacher,
                row[6],
                row[7]
            )

            exercise = Exercise(
                row[0],
                row[1],
                course,
            )

            exercises.append(exercise)

        return exercises


    def count_exercises(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM exercises
        """)

        result = self.db.cursor.fetchone()

        return result[0]

    def get_exercises_by_level(self, level):

        level = level.strip().upper()

        self.db.cursor.execute("""
            SELECT
                exercises.exercise_id,
                exercises.exercise_name,
                exercises.level,
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
            FROM exercises

            JOIN courses
                ON exercises.course_id = courses.course_id

            JOIN teachers
                ON courses.teacher_id = teachers.teacher_id

            WHERE UPPER(TRIM(exercises.level)) = ?
        """, (level,))

        rows = self.db.cursor.fetchall()

        exercises = []

        for row in rows:

            teacher = Teacher(
                row[8],
                row[9],
                row[10],
                row[11],
                row[12]
            )

            course = Course(
                row[3],
                row[4],
                teacher,
                row[6],
                row[7]
            )

            exercise = Exercise(
                row[0],
                row[1],
                course,
            )

            exercises.append(exercise)

        return exercises