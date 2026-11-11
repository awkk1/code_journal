import sqlite3
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from backend.database import get_connection
from backend.schemas import ArticleCreate, ArticleUpdate

router_articles = APIRouter(prefix="/articles")

# Take all articles
@router_articles.get("")
def get_articles() -> list[dict]:
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute("""
            SELECT * FROM articles
            ORDER BY created_at DESC, id DESC;
        """)

        articles = [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()

    return articles

# Get one article by id
@router_articles.get("/{article_id}")
def get_article_by_id(article_id: int) -> dict:
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute(
            "SELECT * from articles WHERE id = ?;",
            (article_id,)
        )

        row = cursor.fetchone()

    finally:
        connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Article not found")

    article = dict(row)

    return article

# Create the article
@router_articles.post("", status_code=201)
def create_article(article: ArticleCreate) -> dict:
    connection = get_connection()

    now = datetime.now(timezone.utc).isoformat()

    try:
        cursor = connection.execute("""
            INSERT INTO articles (title, description, content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)""",
            (article.title, article.description, article.content, now, now)
        )

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()

    article_id = cursor.lastrowid

    created_article = {
        "id": article_id,
        "title": article.title,
        "description": article.description,
        "content": article.content,
        "created_at": now,
        "updated_at": now
    }

    return created_article

# Update the article
@router_articles.patch("/{article_id}")
def update_article(article_id: int, article: ArticleUpdate) -> dict:
    updates = article.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(status_code=422, detail="No fields provided for update")

    now = datetime.now(timezone.utc).isoformat()

    query = "UPDATE articles SET "

    query += ", ".join(f"{key} = ?" for key in updates.keys())

    query += ", updated_at = ? WHERE id = ?;"

    fields = [value for value in updates.values()]
    fields.extend([now, article_id])

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    row = None

    try:
        connection.execute(query, fields)
        connection.commit()

        cursor = connection.execute(
            "SELECT * FROM articles WHERE id = ?;",
            (article_id,)
        )

        row = cursor.fetchone()

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Article not found")

    updated_article = dict(row)

    return updated_article

# Delete article by id
@router_articles.delete("/{article_id}", status_code=204)
def delete_article_by_id(article_id: int) -> None:
    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM articles WHERE id = ?;",
            (article_id,)
        )

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()

    if not cursor.rowcount:
        raise HTTPException(status_code=404, detail="Article not found")

    return