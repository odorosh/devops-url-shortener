from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    # 1. Sprawdzamy dostępność strony głównej
    response = client.get("/")
    assert response.status_code == 200
    assert "Мій DevOps Портал" in response.text

def test_create_and_redirect_link():
    # 2. Tworzymy payload dla formularza HTML
    payload = {
        "short_code": "clean-slate",
        "long_url": "https://getfedora.org"
    }
    # Wysyłamy żądanie POST i sprawdzamy wyłącznie kod statusu 200 OK
    response = client.post("/shorten", data=payload)
    assert response.status_code == 200

    # 3. Sprawdzamy, czy przekierowanie (307 Temporary Redirect) działa poprawnie
    redirect_response = client.get("/clean-slate", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://getfedora.org"
