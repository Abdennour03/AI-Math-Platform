import sqlite3

from models.grade import Grade


class GradeRepo:
    def __init__(self, db, student_repo, exercise_repo):
        self.db = db
        self.student_repo = student_repo
        self.exercise_repo = exercise_repo

    def _from_row(self, row):
        student = self.student_repo.get_student(row[2])
        exercise = self.exercise_repo.get_exercise(row[3])
        if student is None or exercise is None:
            return None
        return Grade(row[0], row[1], student, exercise)

    def add_grade(self, grade):
        try:
            self.db.cursor.execute(
                "INSERT INTO grades (score, student_id, exercise_id) VALUES (?, ?, ?)",
                (grade.score, grade.student.student_id, grade.exercise.exercise_id),
            )
            self.db.connection.commit()
        except sqlite3.IntegrityError as error:
            self.db.connection.rollback()
            if "UNIQUE constraint failed" in str(error):
                raise ValueError("This student already has a grade for this exercise.") from error
            raise
        grade.grade_id = self.db.cursor.lastrowid

    def get_grade_by_student_and_exercise(self, student_id, exercise_id):
        self.db.cursor.execute(
            "SELECT grade_id, score, student_id, exercise_id FROM grades WHERE student_id = ? AND exercise_id = ?",
            (student_id, exercise_id),
        )
        row = self.db.cursor.fetchone()
        return self._from_row(row) if row else None

    def get_grade(self, grade_id):
        self.db.cursor.execute(
            "SELECT grade_id, score, student_id, exercise_id FROM grades WHERE grade_id = ?",
            (grade_id,),
        )
        row = self.db.cursor.fetchone()
        return self._from_row(row) if row else None

    def get_all_grades(self):
        self.db.cursor.execute("SELECT grade_id, score, student_id, exercise_id FROM grades")
        return [grade for row in self.db.cursor.fetchall() if (grade := self._from_row(row))]

    def update_grade(self, grade_id, **kwargs):
        if "score" in kwargs:
            self.db.cursor.execute("UPDATE grades SET score = ? WHERE grade_id = ?", (kwargs["score"], grade_id))
        if "student" in kwargs:
            self.db.cursor.execute("UPDATE grades SET student_id = ? WHERE grade_id = ?", (kwargs["student"].student_id, grade_id))
        if "exercise" in kwargs:
            self.db.cursor.execute("UPDATE grades SET exercise_id = ? WHERE grade_id = ?", (kwargs["exercise"].exercise_id, grade_id))
        try:
            self.db.connection.commit()
        except sqlite3.IntegrityError as error:
            self.db.connection.rollback()
            raise ValueError("This student already has a grade for this exercise.") from error
        return True

    def delete_grade(self, grade_id):
        self.db.cursor.execute("DELETE FROM grades WHERE grade_id = ?", (grade_id,))
        self.db.connection.commit()
        return self.db.cursor.rowcount > 0

    def search_grade_by_student(self, student_id):
        self.db.cursor.execute("SELECT grade_id, score, student_id, exercise_id FROM grades WHERE student_id = ?", (student_id,))
        return [grade for row in self.db.cursor.fetchall() if (grade := self._from_row(row))]

    def search_grade_by_exercises(self, exercise_id):
        self.db.cursor.execute("SELECT grade_id, score, student_id, exercise_id FROM grades WHERE exercise_id = ?", (exercise_id,))
        return [grade for row in self.db.cursor.fetchall() if (grade := self._from_row(row))]

    def search_grade_by_exercise(self, exercise_id):
        return self.search_grade_by_exercises(exercise_id)

    def count_grades(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM grades")
        return self.db.cursor.fetchone()[0]
