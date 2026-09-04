import sqlite3

from models.grad import Grade


class GradeRepo:

    def __init__(self, db, student_repo, exercise_repo):

        self.db = db
        self.student_repo = student_repo
        self.exercise_repo = exercise_repo

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                score REAL NOT NULL,
                student_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,

                FOREIGN KEY (student_id)
                    REFERENCES students(student_id),

                FOREIGN KEY (exercise_id)
                    REFERENCES exercises(exercise_id),

                UNIQUE (student_id, exercise_id)
            )
        """)

        self.db.connection.commit()
        self._enforce_unique_student_exercise()


    def _enforce_unique_student_exercise(self):

        self.db.cursor.execute("""
            SELECT 1
            FROM grades
            GROUP BY student_id, exercise_id
            HAVING COUNT(*) > 1
            LIMIT 1
        """)

        has_duplicates = self.db.cursor.fetchone() is not None

        if not has_duplicates:
            self.db.cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS
                idx_grades_student_exercise
                ON grades(student_id, exercise_id)
            """)

        self.db.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS prevent_duplicate_grade_insert
            BEFORE INSERT ON grades
            WHEN EXISTS (
                SELECT 1
                FROM grades
                WHERE student_id = NEW.student_id
                  AND exercise_id = NEW.exercise_id
            )
            BEGIN
                SELECT RAISE(
                    ABORT,
                    'This student already has a grade for this exercise.'
                );
            END
        """)

        self.db.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS prevent_duplicate_grade_update
            BEFORE UPDATE OF student_id, exercise_id ON grades
            WHEN EXISTS (
                SELECT 1
                FROM grades
                WHERE student_id = NEW.student_id
                  AND exercise_id = NEW.exercise_id
                  AND grade_id != OLD.grade_id
            )
            BEGIN
                SELECT RAISE(
                    ABORT,
                    'This student already has a grade for this exercise.'
                );
            END
        """)

        self.db.connection.commit()


    def add_grade(self, grade):

        try:
            self.db.cursor.execute("""
                INSERT INTO grades
                (score, student_id, exercise_id)
                VALUES (?, ?, ?)
            """, (
                grade.score,
                grade.student.student_id,
                grade.exercise.exercise_id
            ))
        except sqlite3.IntegrityError as error:
            self.db.connection.rollback()
            if "student already has a grade" in str(error):
                raise ValueError(str(error)) from error
            raise

        self.db.connection.commit()

        grade.grade_id = self.db.cursor.lastrowid


    def get_grade_by_student_and_exercise(
        self,
        student_id,
        exercise_id
    ):

        self.db.cursor.execute("""
            SELECT
                grade_id,
                score,
                student_id,
                exercise_id
            FROM grades
            WHERE student_id = ? AND exercise_id = ?
            LIMIT 1
        """, (student_id, exercise_id))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        student = self.student_repo.get_student(row[2])
        exercise = self.exercise_repo.get_exercise(row[3])

        if student is None or exercise is None:
            return None

        return Grade(row[0], row[1], student, exercise)


    def get_grade(self, grade_id):

        self.db.cursor.execute("""
            SELECT
                grade_id,
                score,
                student_id,
                exercise_id
            FROM grades
            WHERE grade_id = ?
        """, (grade_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        student = self.student_repo.get_student(row[2])

        exercise = self.exercise_repo.get_exercise(row[3])

        if student is None or exercise is None:
            return None

        return Grade(
            row[0],
            row[1],
            student,
            exercise
        )


    def get_all_grades(self):

        self.db.cursor.execute("""
            SELECT
                grade_id,
                score,
                student_id,
                exercise_id
            FROM grades
        """)

        rows = self.db.cursor.fetchall()

        grades = []

        for row in rows:

            student = self.student_repo.get_student(row[2])

            exercise = self.exercise_repo.get_exercise(row[3])

            if student is None or exercise is None:
                continue

            grade = Grade(
                row[0],
                row[1],
                student,
                exercise
            )

            grades.append(grade)

        return grades


    def update_grade(self, grade_id, **kwargs):

        try:
            if "score" in kwargs:

                self.db.cursor.execute("""
                    UPDATE grades
                    SET score = ?
                    WHERE grade_id = ?
                """, (
                    kwargs["score"],
                    grade_id
                ))


            if "student" in kwargs:

                self.db.cursor.execute("""
                    UPDATE grades
                    SET student_id = ?
                    WHERE grade_id = ?
                """, (
                    kwargs["student"].student_id,
                    grade_id
                ))


            if "exercise" in kwargs:

                self.db.cursor.execute("""
                    UPDATE grades
                    SET exercise_id = ?
                    WHERE grade_id = ?
                """, (
                    kwargs["exercise"].exercise_id,
                    grade_id
                ))
        except sqlite3.IntegrityError as error:
            self.db.connection.rollback()
            if "student already has a grade" in str(error):
                raise ValueError(str(error)) from error
            raise


        self.db.connection.commit()

        return True


    def delete_grade(self, grade_id):

        grade = self.get_grade(grade_id)

        if grade is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM grades
            WHERE grade_id = ?
        """, (grade_id,))

        self.db.connection.commit()

        return True


    def search_grade_by_student(self, student_id):

        self.db.cursor.execute("""
            SELECT
                grade_id,
                score,
                student_id,
                exercise_id
            FROM grades
            WHERE student_id = ?
        """, (student_id,))

        rows = self.db.cursor.fetchall()

        grades = []

        for row in rows:

            student = self.student_repo.get_student(row[2])

            exercise = self.exercise_repo.get_exercise(row[3])

            if student is None or exercise is None:
                continue

            grade = Grade(
                row[0],
                row[1],
                student,
                exercise
            )

            grades.append(grade)

        return grades


    def search_grade_by_exercises(self, exercise_id):

        self.db.cursor.execute("""
            SELECT
                grade_id,
                score,
                student_id,
                exercise_id
            FROM grades
            WHERE exercise_id = ?
        """, (exercise_id,))

        rows = self.db.cursor.fetchall()

        grades = []

        for row in rows:

            student = self.student_repo.get_student(row[2])

            exercise = self.exercise_repo.get_exercise(row[3])

            if student is None or exercise is None:
                continue

            grade = Grade(
                row[0],
                row[1],
                student,
                exercise
            )

            grades.append(grade)

        return grades


    def count_grades(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM grades
        """)

        result = self.db.cursor.fetchone()

        return result[0]
    