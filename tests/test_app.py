from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "DevOps Demo API",
        "version": "0.1.1",
    }


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_metrics_endpoint_exposes_request_metrics():
    client = TestClient(app)

    client.get("/")

    response = client.get("/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert 'endpoint="/"' in response.text
    assert "http_request_duration_seconds" in response.text

