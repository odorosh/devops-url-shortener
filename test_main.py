from fastapi.testclient import TestClient
from main import app

# Створюємо віртуального клієнта для тестування нашого додатка
client = TestClient(app)

def test_read_main():
    # 1. Робимо запит до головної сторінки
    response = client.get("/")
    # 2. Перевіряємо, чи сервер відповідає кодом 200 (Все OK)
    assert response.status_code == 200
    # 3. Перевіряємо, чи є на сторінці наш текст
    assert "Мій DevOps Портал" in response.text

def test_redirect_link():
    # Перевіряємо, чи працює редірект для стандартного посилання 'fedora'
    response = client.get("/fedora", follow_redirects=False)
    assert response.status_code == 307  # Тимчасовий редірект
