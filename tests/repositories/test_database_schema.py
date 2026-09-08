from database.database import Database


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
