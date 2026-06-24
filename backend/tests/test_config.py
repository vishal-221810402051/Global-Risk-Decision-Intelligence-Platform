from app.core.config import settings


def test_local_frontend_origins_allow_localhost_and_loopback() -> None:
    assert "http://localhost:5173" in settings.frontend_origins
    assert "http://127.0.0.1:5173" in settings.frontend_origins
