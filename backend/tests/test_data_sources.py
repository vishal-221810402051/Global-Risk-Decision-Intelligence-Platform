import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture()
def client() -> TestClient:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Session:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    test_client = TestClient(app)
    yield test_client
    test_client.close()

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def sample_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "source_id": "open_meteo_weather",
        "source_name": "Open-Meteo Weather Forecast API",
        "source_url": "https://open-meteo.com/",
        "dataset_type": "weather",
        "sector": "multi_sector",
        "country_scope": ["India", "France", "Kenya"],
        "refresh_frequency": "hourly",
        "reliability_score": 85,
        "active_flag": True,
        "last_updated": None,
        "notes": "Candidate weather source metadata only. No ingestion in Phase 2.",
    }
    payload.update(overrides)
    return payload


def create_source(client: TestClient, **overrides: object) -> dict[str, object]:
    response = client.post("/data-sources", json=sample_payload(**overrides))
    assert response.status_code == 201
    return response.json()


def test_list_empty_registry(client: TestClient) -> None:
    response = client.get("/data-sources")

    assert response.status_code == 200
    assert response.json() == []


def test_create_data_source(client: TestClient) -> None:
    response = client.post("/data-sources", json=sample_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["source_id"] == "open_meteo_weather"
    assert body["reliability_score"] == 85
    assert body["created_at"]
    assert body["updated_at"]


def test_get_data_source_by_id(client: TestClient) -> None:
    create_source(client)

    response = client.get("/data-sources/open_meteo_weather")

    assert response.status_code == 200
    assert response.json()["source_name"] == "Open-Meteo Weather Forecast API"


def test_duplicate_source_id_rejected(client: TestClient) -> None:
    create_source(client)

    response = client.post("/data-sources", json=sample_payload())

    assert response.status_code == 409


def test_reliability_score_validation(client: TestClient) -> None:
    response = client.post("/data-sources", json=sample_payload(reliability_score=101))

    assert response.status_code == 422


def test_dataset_type_validation(client: TestClient) -> None:
    response = client.post("/data-sources", json=sample_payload(dataset_type="transport"))

    assert response.status_code == 422


def test_sector_validation(client: TestClient) -> None:
    response = client.post("/data-sources", json=sample_payload(sector="health"))

    assert response.status_code == 422


def test_filter_by_active_only(client: TestClient) -> None:
    create_source(client, source_id="active_weather", active_flag=True)
    create_source(client, source_id="inactive_weather", active_flag=False)

    response = client.get("/data-sources?active_only=true")

    assert response.status_code == 200
    assert [item["source_id"] for item in response.json()] == ["active_weather"]


def test_filter_by_country(client: TestClient) -> None:
    create_source(client, source_id="india_weather", country_scope=["India"])
    create_source(client, source_id="france_weather", country_scope=["France"])

    response = client.get("/data-sources?country=France")

    assert response.status_code == 200
    assert [item["source_id"] for item in response.json()] == ["france_weather"]


def test_patch_active_flag(client: TestClient) -> None:
    create_source(client)

    response = client.patch("/data-sources/open_meteo_weather", json={"active_flag": False})

    assert response.status_code == 200
    assert response.json()["active_flag"] is False


def test_patch_notes_and_reliability_score(client: TestClient) -> None:
    create_source(client)

    response = client.patch(
        "/data-sources/open_meteo_weather",
        json={"notes": "Reviewed source metadata.", "reliability_score": 90},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["notes"] == "Reviewed source metadata."
    assert body["reliability_score"] == 90


def test_missing_source_returns_404(client: TestClient) -> None:
    response = client.get("/data-sources/missing_source")

    assert response.status_code == 404


def test_patch_missing_source_returns_404(client: TestClient) -> None:
    response = client.patch("/data-sources/missing_source", json={"active_flag": False})

    assert response.status_code == 404
