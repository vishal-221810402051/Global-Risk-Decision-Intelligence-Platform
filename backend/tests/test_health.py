from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_mvp_contract() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Global Risk Decision Intelligence Platform API",
        "version": "0.1.0",
        "phase": "Phase 1 - Base App Setup",
        "mvp_countries": ["India", "France", "Kenya"],
        "mvp_sectors": ["Agriculture", "Energy"],
    }
