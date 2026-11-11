import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True, parents=True)

DATABASE_PATH = DATABASE_DIR / "code_journal.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    return connection

def init_db():
    connection = get_connection()

    try:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """)

    finally:
        connection.close()

if __name__ == "__main__":
    init_db()