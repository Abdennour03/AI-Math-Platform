from models.class_group import ClassGroup


class ClassRepo:
    def __init__(self, db):
        self.db = db

    def add_class(self, class_group):
        next_id = self.db.cursor.execute(
            "SELECT COALESCE(MAX(id), 0) + 1 FROM classes"
        ).fetchone()[0]
        self.db.cursor.execute(
            "INSERT INTO classes (id, name, academic_year) VALUES (?, ?, ?)",
            (next_id, class_group.name, class_group.academic_year),
        )
        self.db.connection.commit()
        class_group.class_id = self.db.cursor.lastrowid

    def get_class(self, class_id):
        self.db.cursor.execute(
            "SELECT id, name, academic_year FROM classes WHERE id = ?",
            (class_id,),
        )
        row = self.db.cursor.fetchone()
        return ClassGroup(*row) if row else None

    def get_all_classes(self):
        self.db.cursor.execute(
            "SELECT id, name, academic_year FROM classes ORDER BY name"
        )
        return [ClassGroup(*row) for row in self.db.cursor.fetchall()]

    def search_classes(self, query):
        self.db.cursor.execute(
            """SELECT id, name, academic_year FROM classes
               WHERE name LIKE ? OR academic_year LIKE ? ORDER BY name""",
            (f"%{query}%", f"%{query}%"),
        )
        return [ClassGroup(*row) for row in self.db.cursor.fetchall()]

    def update_class(self, class_id, **updates):
        fields = [field for field in ("name", "academic_year") if field in updates]
        if fields:
            values = [updates[field] for field in fields] + [class_id]
            self.db.cursor.execute(
                f"UPDATE classes SET {', '.join(f'{field} = ?' for field in fields)} WHERE id = ?",
                values,
            )
            self.db.connection.commit()

    def delete_class(self, class_id):
        self.db.cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
        deleted = self.db.cursor.rowcount > 0
        self.db.connection.commit()
        return deleted