from database.database import Database
from models.student import Student
from repositories.student_repository import StudentRepo


def test_database_creates_core_schema(tmp_path):
    db = Database(str(tmp_path / "schema.db"))
    tables = {
        row[0]
        for row in db.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    assert {"students", "teachers", "courses", "exercises", "grades"} <= tables
    assert db.cursor.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    db.close()


def test_student_academic_report_joins_class_by_id(tmp_path):
    db = Database(str(tmp_path / "report.db"))
    db.cursor.execute(
        "INSERT INTO classes (name, academic_year) VALUES (?, ?)",
        ("3ac math", "3AC"),
    )
    class_id = db.cursor.lastrowid
    student = Student(
        None,
        "Yassin",
        "yassin@example.com",
        "password",
        "0679120023",
        "3AC",
        class_id,
    )
    StudentRepo(db).add_student(student)
    db.cursor.execute(
        "INSERT INTO teachers (full_name, email, password, phone_number) VALUES (?, ?, ?, ?)",
        ("Teacher", "teacher@example.com", "password", "0600000000"),
    )
    teacher_id = db.cursor.lastrowid
    db.cursor.execute(
        "INSERT INTO courses (course_name, teacher_id, semester, level) VALUES (?, ?, ?, ?)",
        ("Mathematics", teacher_id, "S1", "3ac math"),
    )
    course_id = db.cursor.lastrowid
    db.cursor.execute(
        "INSERT INTO exercises (exercise_name, course_id, max_score) VALUES (?, ?, ?)",
        ("Algebra test", course_id, 20),
    )
    exercise_id = db.cursor.lastrowid
    db.cursor.execute(
        "INSERT INTO grades (score, student_id, exercise_id) VALUES (?, ?, ?)",
        (17, student.student_id, exercise_id),
    )
    db.connection.commit()

    report = StudentRepo(db).get_academic_report(student.student_id)

    assert report["class_info"] == {
        "class_id": class_id,
        "name": "3ac math",
        "academic_year": "3AC",
    }
    assert report["exercises_and_exams"] == [{
        "exercise_id": exercise_id,
        "exercise_name": "Algebra test",
        "score": 17.0,
    }]
    db.close()
