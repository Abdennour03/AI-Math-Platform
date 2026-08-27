from models.submission import Submission
from models.exercise import Exercise
from models.course import Course
from models.teacher import Teacher
from models.student import Student


class SubmissionRepo:

    def __init__(self, db, student_repo, exercise_repo):
        self.db = db
        self.student_repo = student_repo
        self.exercise_repo = exercise_repo

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                submission_date TEXT NOT NULL,
                file_path TEXT NOT NULL,
                status TEXT NOT NULL,

                FOREIGN KEY (student_id)
                    REFERENCES students(student_id),

                FOREIGN KEY (exercise_id)
                    REFERENCES exercises(exercise_id)
            )
        """)

        self.db.connection.commit()


    def add_submission(self, submission):

        self.db.cursor.execute("""
            INSERT INTO submissions
            (
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            submission.student_id,
            submission.exercise.exercise_id,
            submission.submission_date,
            submission.file_path,
            submission.status
        ))

        self.db.connection.commit()

        submission.submission_id = self.db.cursor.lastrowid


    def get_submission(self, submission_id):

        self.db.cursor.execute("""
            SELECT
                submission_id,
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            FROM submissions
            WHERE submission_id = ?
        """, (submission_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        student = self.student_repo.get_student(row[1])

        exercise = self.exercise_repo.get_exercise(row[2])

        if student is None or exercise is None:
            return None

        return Submission(
            row[0],
            student.student_id,
            exercise,
            row[3],
            row[4],
            row[5]
        )


    def get_all_submissions(self):

        self.db.cursor.execute("""
            SELECT
                submission_id,
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            FROM submissions
        """)

        rows = self.db.cursor.fetchall()

        submissions = []

        for row in rows:

            student = self.student_repo.get_student(row[1])

            exercise = self.exercise_repo.get_exercise(row[2])

            if student is None or exercise is None:
                continue

            submission = Submission(
                row[0],
                student.student_id,
                exercise,
                row[3],
                row[4],
                row[5]
            )

            submissions.append(submission)

        return submissions


    def update_submission(self, submission_id, **kwargs):

        if "student_id" in kwargs:

            self.db.cursor.execute("""
                UPDATE submissions
                SET student_id = ?
                WHERE submission_id = ?
            """, (
                kwargs["student_id"],
                submission_id
            ))


        if "exercise" in kwargs:

            self.db.cursor.execute("""
                UPDATE submissions
                SET exercise_id = ?
                WHERE submission_id = ?
            """, (
                kwargs["exercise"].exercise_id,
                submission_id
            ))


        if "submission_date" in kwargs:

            self.db.cursor.execute("""
                UPDATE submissions
                SET submission_date = ?
                WHERE submission_id = ?
            """, (
                kwargs["submission_date"],
                submission_id
            ))


        if "file_path" in kwargs:

            self.db.cursor.execute("""
                UPDATE submissions
                SET file_path = ?
                WHERE submission_id = ?
            """, (
                kwargs["file_path"],
                submission_id
            ))


        if "status" in kwargs:

            self.db.cursor.execute("""
                UPDATE submissions
                SET status = ?
                WHERE submission_id = ?
            """, (
                kwargs["status"],
                submission_id
            ))


        self.db.connection.commit()

        return True


    def delete_submission(self, submission_id):

        submission = self.get_submission(submission_id)

        if submission is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM submissions
            WHERE submission_id = ?
        """, (submission_id,))

        self.db.connection.commit()

        return True


    def search_submission_by_student(self, student_id):

        self.db.cursor.execute("""
            SELECT
                submission_id,
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            FROM submissions
            WHERE student_id = ?
        """, (student_id,))

        rows = self.db.cursor.fetchall()

        submissions = []

        for row in rows:

            exercise = self.exercise_repo.get_exercise(row[2])

            if exercise is None:
                continue

            submission = Submission(
                row[0],
                row[1],
                exercise,
                row[3],
                row[4],
                row[5]
            )

            submissions.append(submission)

        return submissions


    def search_submission_by_exercise(self, exercise_id):

        self.db.cursor.execute("""
            SELECT
                submission_id,
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            FROM submissions
            WHERE exercise_id = ?
        """, (exercise_id,))

        rows = self.db.cursor.fetchall()

        submissions = []

        for row in rows:

            submission = Submission(
                row[0],
                row[1],
                self.exercise_repo.get_exercise(row[2]),
                row[3],
                row[4],
                row[5]
            )

            submissions.append(submission)

        return submissions


    def count_submissions(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM submissions
        """)

        result = self.db.cursor.fetchone()

        return result[0]

    def get_submissions_by_student(self, student_id):

        self.db.cursor.execute("""
            SELECT
                submission_id,
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            FROM submissions
            WHERE student_id = ?
        """, (student_id,))

        rows = self.db.cursor.fetchall()

        submissions = []

        for row in rows:

            exercise = self.exercise_repo.get_exercise(row[2])

            if exercise is None:
                continue

            submission = Submission(
                row[0],
                row[1],
                exercise,
                row[3],
                row[4],
                row[5]
            )

            submissions.append(submission)

        return submissions