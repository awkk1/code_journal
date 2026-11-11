from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_articles(test_db):
    response = client.get("/articles")

    titles = [article["title"] for article in response.json()]

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert set(titles) == {"Python", "FastAPI", "SQLite"}

def test_get_article_by_id(test_db):
    response = client.get("/articles/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Python"

def test_get_article_not_found(test_db):
    response = client.get("/articles/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Article not found"}

def test_create_article(test_db):
    data = {
        "title": "USA",
        "description": "Hollow night",
        "content": "Easy weekends"
    }

    response = client.post("/articles", json=data)

    assert response.status_code == 201
    assert response.json()["title"] == "USA"
    assert response.json()["id"] == 4
    assert response.json()["description"] == "Hollow night"
    assert response.json()["content"] == "Easy weekends"
    assert response.json()["created_at"]
    assert response.json()["updated_at"] == response.json()["created_at"]

    get_response = client.get("/articles")

    assert get_response.status_code == 200
    assert len(get_response.json()) == 4

def test_create_article_without_description(test_db):
    data = {
        "title": "America",
        "content": "Good Night and Funny Games"
    }

    response = client.post("/articles", json=data)

    assert response.status_code == 201
    assert response.json()["title"] == "America"
    assert response.json()["id"] == 4
    assert response.json()["description"] is None
    assert response.json()["content"] == "Good Night and Funny Games"
    assert response.json()["created_at"]
    assert response.json()["updated_at"] == response.json()["created_at"]

    get_response = client.get("/articles")
    
    assert get_response.status_code == 200
    assert len(get_response.json()) == 4

def test_update_article(test_db):
    article = client.get("/articles/1")

    assert article.status_code == 200
    
    data = {
        "title": "Advanced Python"
    }

    response = client.patch("/articles/1", json=data)

    assert response.status_code == 200
    assert response.json()["title"] == "Advanced Python"
    assert response.json()["description"] == article.json()["description"]
    assert response.json()["content"] == article.json()["content"]
    assert response.json()["created_at"] == article.json()["created_at"]
    assert response.json()["updated_at"] != article.json()["updated_at"]

    new_article_title = client.get("/articles/1")

    assert new_article_title.status_code == 200
    assert new_article_title.json()["title"] == "Advanced Python"

def test_update_article_empty(test_db):
    response = client.patch("/articles/1", json={})

    assert response.status_code == 422
    assert response.json() == {"detail": "No fields provided for update"}

def test_update_article_not_found(test_db):
    data = {
        "title": "good"
    }

    response = client.patch("/articles/9999", json=data)

    assert response.status_code == 404
    assert response.json() == {"detail": "Article not found"}

def test_delete_article(test_db):
    response = client.delete("/articles/1")

    assert response.status_code == 204
    assert response.content == b""

    check_art = client.get("/articles")

    assert check_art.status_code == 200
    assert len(check_art.json()) == 2

def test_delete_article_not_found(test_db):
    response = client.delete("/articles/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Article not found"}

def test_update_title_null(test_db):
    data = {"title": None}

    response = client.patch("/articles/1", json=data)

    assert response.status_code == 422

def test_update_content_null(test_db):
    data = {"content": None}
    
    response = client.patch("/articles/1", json=data)

    assert response.status_code == 422

def test_update_description_null(test_db):
    data = {"description": None}
    
    response = client.patch("/articles/1", json=data)

    assert response.status_code == 200