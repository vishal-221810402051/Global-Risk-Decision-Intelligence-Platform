from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.open_meteo_client import OpenMeteoClient, WeatherProviderError
from app.services.weather_service import get_weather


client = TestClient(app)


class FakeOpenMeteoClient:
    def __init__(self, payload: dict[str, Any] | None = None, error: Exception | None = None) -> None:
        self.payload = payload or {}
        self.error = error

    def fetch(self, latitude: float, longitude: float, mode: str) -> dict[str, Any]:
        if self.error:
            raise self.error
        return self.payload


def current_payload() -> dict[str, Any]:
    return {
        "latitude": 28.61,
        "longitude": 77.2,
        "elevation": 216,
        "generationtime_ms": 1.2,
        "utc_offset_seconds": 19800,
        "timezone": "Asia/Kolkata",
        "timezone_abbreviation": "IST",
        "current_units": {
            "time": "iso8601",
            "interval": "seconds",
            "temperature_2m": "°C",
            "precipitation": "mm",
            "wind_speed_10m": "km/h",
        },
        "current": {
            "time": "2026-06-24T15:00",
            "interval": 900,
            "temperature_2m": 38.4,
            "precipitation": 0.0,
            "wind_speed_10m": 12.5,
        },
    }


def forecast_payload() -> dict[str, Any]:
    return {
        "latitude": 48.85,
        "longitude": 2.35,
        "elevation": 35,
        "generationtime_ms": 1.5,
        "utc_offset_seconds": 7200,
        "timezone": "Europe/Paris",
        "timezone_abbreviation": "CEST",
        "hourly_units": {
            "time": "iso8601",
            "temperature_2m": "°C",
            "precipitation": "mm",
        },
        "hourly": {
            "time": ["2026-06-24T00:00", "2026-06-24T01:00"],
            "temperature_2m": [27.1, 26.4],
            "precipitation": [0.0, 0.2],
        },
        "daily_units": {
            "time": "iso8601",
            "temperature_2m_max": "°C",
            "rain_sum": "mm",
        },
        "daily": {
            "time": ["2026-06-24"],
            "temperature_2m_max": [31.2],
            "rain_sum": [0.8],
        },
    }


def test_request_params_are_built_correctly() -> None:
    client = OpenMeteoClient(api_key="test-key")

    params = client.build_request_params(28.6139, 77.209, "forecast")

    assert params["latitude"] == 28.6139
    assert params["longitude"] == 77.209
    assert params["hourly"] == "temperature_2m,precipitation,rain,soil_moisture_0_to_1cm,soil_moisture_1_to_3cm"
    assert params["daily"] == "temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum"
    assert params["forecast_days"] == 3
    assert params["apikey"] == "test-key"


def test_current_provider_response_normalizes_to_real_records() -> None:
    response = get_weather("India", "current", client=FakeOpenMeteoClient(current_payload()))

    assert response.fallback_used is False
    assert response.provider == "open_meteo"
    assert response.records
    assert all(record.is_mock is False for record in response.records)
    assert {record.variable for record in response.records} == {"temperature_2m", "precipitation", "wind_speed_10m"}


def test_timeout_uses_mock_fallback_when_enabled() -> None:
    response = get_weather(
        "India",
        "current",
        client=FakeOpenMeteoClient(error=WeatherProviderError("timeout")),
        use_mock_fallback=True,
    )

    assert response.fallback_used is True
    assert response.provider == "mock_data"
    assert response.records
    assert all(record.is_mock is True for record in response.records)


def test_timeout_returns_clean_error_when_fallback_disabled() -> None:
    with pytest.raises(WeatherProviderError):
        get_weather(
            "India",
            "current",
            client=FakeOpenMeteoClient(error=WeatherProviderError("timeout")),
            use_mock_fallback=False,
        )


def test_invalid_country_handled_cleanly() -> None:
    response = client.get("/weather/current?country=Brazil")

    assert response.status_code == 400


def test_units_are_preserved() -> None:
    response = get_weather("India", "current", client=FakeOpenMeteoClient(current_payload()))

    units = {record.variable: record.unit for record in response.records}
    assert units["temperature_2m"] == "°C"
    assert units["precipitation"] == "mm"
    assert units["wind_speed_10m"] == "km/h"


def test_forecast_provider_response_normalizes_hourly_and_daily_records() -> None:
    response = get_weather("France", "forecast", client=FakeOpenMeteoClient(forecast_payload()))

    assert response.fallback_used is False
    assert len(response.records) == 6
    assert all(record.is_mock is False for record in response.records)
    assert any(record.variable == "temperature_2m" for record in response.records)
    assert any(record.variable == "temperature_2m_max" for record in response.records)


def test_current_weather_endpoint_uses_mock_fallback_for_provider_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def raise_provider_error(self: OpenMeteoClient, latitude: float, longitude: float, mode: str) -> dict[str, Any]:
        raise WeatherProviderError("timeout")

    monkeypatch.setattr(OpenMeteoClient, "fetch", raise_provider_error)

    response = client.get("/weather/current?country=Kenya")

    assert response.status_code == 200
    body = response.json()
    assert body["fallback_used"] is True
    assert body["records"]
    assert all(record["is_mock"] is True for record in body["records"])
