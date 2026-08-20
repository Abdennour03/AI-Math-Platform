import sqlite3
import os

class Database:
    def __init__(self, db_name="eduinsight.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()


    def create_tables(self):
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    phone_number TEXT,
    level TEXT NOT NULL
    )
        """)
        self.connection.commit()


    def close(self):
        self.connection.close()