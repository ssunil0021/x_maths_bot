import sqlite3

def init_db():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unique_code TEXT,
            date TEXT,
            question_drive_id TEXT,
            solution_drive_id TEXT,
            solution_released INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
