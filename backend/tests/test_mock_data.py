from fastapi.testclient import TestClient

from app.main import app
from app.services import mock_data_service


client = TestClient(app)


def test_country_baseline_loading() -> None:
    records = mock_data_service.get_country_baselines()

    assert len(records) == 3
    assert {record.country for record in records} == {"India", "France", "Kenya"}


def test_weather_signal_loading() -> None:
    records = mock_data_service.get_weather_signals()

    assert records
    assert any(record.signal_type == "rainfall_deficit" for record in records)


def test_agriculture_signal_loading() -> None:
    records = mock_data_service.get_agriculture_signals()

    assert records
    assert all(record.sector == "Agriculture" for record in records)


def test_energy_signal_loading() -> None:
    records = mock_data_service.get_energy_signals()

    assert records
    assert all(record.sector == "Energy" for record in records)


def test_economy_context_loading() -> None:
    records = mock_data_service.get_economy_context_signals()

    assert records
    assert all(record.sector == "Economy" for record in records)


def test_combined_signals_endpoint() -> None:
    response = client.get("/mock-data/signals")

    assert response.status_code == 200
    assert len(response.json()) == 13


def test_country_filter() -> None:
    response = client.get("/mock-data/signals?country=India")

    assert response.status_code == 200
    assert {record["country"] for record in response.json()} == {"India"}


def test_country_filter_is_case_insensitive() -> None:
    response = client.get("/mock-data/signals?country=india")

    assert response.status_code == 200
    assert {record["country"] for record in response.json()} == {"India"}


def test_sector_filter_accepts_title_case() -> None:
    response = client.get("/mock-data/signals?sector=Energy")

    assert response.status_code == 200
    assert {record["sector"] for record in response.json()} == {"Energy"}


def test_sector_filter_accepts_lowercase() -> None:
    response = client.get("/mock-data/signals?sector=agriculture")

    assert response.status_code == 200
    assert response.json()
    assert {record["sector"] for record in response.json()} == {"Agriculture"}


def test_sector_filter_accepts_uppercase() -> None:
    response = client.get("/mock-data/signals?sector=ENERGY")

    assert response.status_code == 200
    assert response.json()
    assert {record["sector"] for record in response.json()} == {"Energy"}


def test_signal_type_filter() -> None:
    response = client.get("/mock-data/signals?signal_type=rainfall_deficit")

    assert response.status_code == 200
    assert response.json()
    assert {record["signal_type"] for record in response.json()} == {"rainfall_deficit"}


def test_signal_type_filter_is_case_insensitive() -> None:
    response = client.get("/mock-data/signals?signal_type=Rainfall_Deficit")

    assert response.status_code == 200
    assert response.json()
    assert {record["signal_type"] for record in response.json()} == {"rainfall_deficit"}


def test_invalid_sector_filter_returns_empty_list() -> None:
    response = client.get("/mock-data/signals?sector=health")

    assert response.status_code == 200
    assert response.json() == []


def test_all_records_have_is_mock_true() -> None:
    baseline_response = client.get("/mock-data/countries")
    signal_response = client.get("/mock-data/signals")

    assert all(record["is_mock"] is True for record in baseline_response.json())
    assert all(record["is_mock"] is True for record in signal_response.json())


def test_invalid_country_filter_behavior() -> None:
    response = client.get("/mock-data/signals?country=Brazil")

    assert response.status_code == 200
    assert response.json() == []


def test_no_write_endpoints_exist() -> None:
    assert client.post("/mock-data/signals", json={}).status_code == 405
    assert client.patch("/mock-data/signals", json={}).status_code == 405
    assert client.delete("/mock-data/signals").status_code == 405


def test_category_endpoints_load() -> None:
    endpoints = [
        "/mock-data/countries",
        "/mock-data/weather",
        "/mock-data/agriculture",
        "/mock-data/energy",
        "/mock-data/economy-context",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.json()
