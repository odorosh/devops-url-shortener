from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    # 1. Перевіряємо доступність головної сторінки
    response = client.get("/")
    assert response.status_code == 200
    assert "Мій DevOps Портал" in response.text

def test_create_and_redirect_link():
    # 2. Самі створюємо тестове посилання в базі через форму (імітуємо дію користувача)
    payload = {
        "short_code": "fedora-test",
        "long_url": "https://getfedora.org"
    }
    # Відправляємо дані як класичну HTML-форму
    response = client.post("/shorten", data=payload)
    assert response.status_code == 200
    assert "Дані успішно збережено в PostgreSQL!" in response.text

    # 3. Перевіряємо, чи працює редірект для щойно створеного посилання
    redirect_response = client.get("/fedora-test", follow_redirects=False)
    assert redirect_response.status_code == 307  # Перевіряємо код редіректу
