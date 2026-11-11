from datetime import datetime, timezone
import pytest
import backend.database as database

@pytest.fixture
def test_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test_code_journal.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_db_path
    )

    database.init_db()

    test_articles = [
    ("Python", "Основы Python", "Текст первой статьи"),
    ("FastAPI", None, "Текст второй статьи"),
    ("SQLite", "Работа с БД", "Текст третьей статьи")
]

    now = datetime.now(timezone.utc).isoformat()

    connection = database.get_connection()

    for article in test_articles:
        connection.execute("""
            INSERT INTO articles (title, description, content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)""",
            (*article, now, now)
        )

    connection.commit()

    connection.close()

    yield