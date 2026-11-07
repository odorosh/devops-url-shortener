import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Мій DevOps Портал" in response.text

def test_create_and_redirect_link():
    payload = {
        "short_code": "clean-slate",
        "long_url": "https://getfedora.org"
    }

    # Wyczyszczenie sesji klienta przed nowym testem
    with TestClient(app) as local_client:
        response = local_client.post("/shorten", data=payload)
        assert response.status_code == 200

        # Dajemy bazie 0.1 sekundy na fizyczny zapis na dysku w chmurze
        time.sleep(0.1)

        redirect_response = local_client.get("/clean-slate", follow_redirects=False)
        assert redirect_response.status_code == 307
        assert redirect_response.headers["location"] == "https://getfedora.org"
