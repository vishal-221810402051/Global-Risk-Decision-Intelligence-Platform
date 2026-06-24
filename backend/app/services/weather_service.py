from datetime import UTC, date, datetime
from typing import Any, Literal

from app.core.config import settings
from app.schemas.mock_data import MockSignal
from app.schemas.weather import WeatherRecord, WeatherResponse
from app.services import mock_data_service
from app.services.open_meteo_client import OpenMeteoClient, WeatherProviderError


OPEN_METEO_SOURCE_ID = "open_meteo_weather"
MOCK_WEATHER_SOURCE_ID = "mock_weather_source"

COUNTRY_COORDINATES = {
    "india": {
        "country": "India",
        "region": "New Delhi",
        "latitude": 28.6139,
        "longitude": 77.2090,
    },
    "france": {
        "country": "France",
        "region": "Paris",
        "latitude": 48.8566,
        "longitude": 2.3522,
    },
    "kenya": {
        "country": "Kenya",
        "region": "Nairobi",
        "latitude": -1.2921,
        "longitude": 36.8219,
    },
}


class UnsupportedCountryError(ValueError):
    pass


def _location_for_country(country: str) -> dict[str, str | float]:
    location = COUNTRY_COORDINATES.get(country.strip().casefold())
    if location is None:
        raise UnsupportedCountryError(f"Unsupported country: {country}")
    return location


def _parse_datetime(value: str) -> datetime:
    if "T" not in value:
        return datetime.combine(date.fromisoformat(value), datetime.min.time(), tzinfo=UTC)
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def _record_metadata(payload: dict[str, Any], section: str, variable: str) -> dict[str, Any]:
    return {
        "provider_section": section,
        "variable": variable,
        "timezone": payload.get("timezone"),
        "timezone_abbreviation": payload.get("timezone_abbreviation"),
        "utc_offset_seconds": payload.get("utc_offset_seconds"),
        "elevation": payload.get("elevation"),
        "generationtime_ms": payload.get("generationtime_ms"),
    }


def _normalize_current_records(payload: dict[str, Any], location: dict[str, str | float]) -> list[WeatherRecord]:
    current = payload.get("current") or {}
    current_units = payload.get("current_units") or {}
    observed_at = _parse_datetime(current["time"]) if current.get("time") else None
    records: list[WeatherRecord] = []

    for variable, value in current.items():
        if variable in {"time", "interval"} or value is None:
            continue
        records.append(
            WeatherRecord(
                provider=settings.weather_provider,
                source_id=OPEN_METEO_SOURCE_ID,
                country=str(location["country"]),
                region=str(location["region"]),
                latitude=float(location["latitude"]),
                longitude=float(location["longitude"]),
                variable=variable,
                value=float(value),
                unit=str(current_units.get(variable, "")),
                observed_at=observed_at,
                forecast_time=None,
                is_mock=False,
                raw_provider_metadata=_record_metadata(payload, "current", variable),
            )
        )

    return records


def _normalize_timeseries_records(
    payload: dict[str, Any],
    location: dict[str, str | float],
    section: Literal["hourly", "daily"],
) -> list[WeatherRecord]:
    values = payload.get(section) or {}
    units = payload.get(f"{section}_units") or {}
    times = values.get("time") or []
    records: list[WeatherRecord] = []

    for variable, series in values.items():
        if variable == "time":
            continue
        for index, value in enumerate(series):
            if value is None:
                continue
            records.append(
                WeatherRecord(
                    provider=settings.weather_provider,
                    source_id=OPEN_METEO_SOURCE_ID,
                    country=str(location["country"]),
                    region=str(location["region"]),
                    latitude=float(location["latitude"]),
                    longitude=float(location["longitude"]),
                    variable=variable,
                    value=float(value),
                    unit=str(units.get(variable, "")),
                    observed_at=None,
                    forecast_time=_parse_datetime(times[index]),
                    is_mock=False,
                    raw_provider_metadata=_record_metadata(payload, section, variable),
                )
            )

    return records


def _mock_signal_to_weather_record(signal: MockSignal, location: dict[str, str | float]) -> WeatherRecord:
    return WeatherRecord(
        provider="mock_data",
        source_id=signal.source_id,
        country=signal.country,
        region=signal.region,
        latitude=float(location["latitude"]),
        longitude=float(location["longitude"]),
        variable=signal.signal_type,
        value=signal.value,
        unit=signal.unit,
        observed_at=signal.timestamp,
        forecast_time=None,
        is_mock=True,
        raw_provider_metadata={
            "fallback_source": "data/mock/weather_signals.json",
            "severity_hint": signal.severity_hint,
            "confidence": signal.confidence,
            "notes": signal.notes,
        },
    )


def _fallback_response(country: str, reason: str, mode: Literal["current", "forecast"]) -> WeatherResponse:
    location = _location_for_country(country)
    mock_records = mock_data_service.list_weather_signals(country=str(location["country"]))
    records = [_mock_signal_to_weather_record(signal, location) for signal in mock_records]

    return WeatherResponse(
        provider="mock_data",
        source_id=MOCK_WEATHER_SOURCE_ID,
        country=str(location["country"]),
        region=str(location["region"]),
        latitude=float(location["latitude"]),
        longitude=float(location["longitude"]),
        fallback_used=True,
        fallback_reason=f"{mode} provider unavailable: {reason}",
        records=records,
    )


def get_weather(
    country: str,
    mode: Literal["current", "forecast"],
    client: OpenMeteoClient | None = None,
    use_mock_fallback: bool = settings.open_meteo_use_mock_fallback,
) -> WeatherResponse:
    location = _location_for_country(country)
    provider_client = client or OpenMeteoClient()

    try:
        payload = provider_client.fetch(float(location["latitude"]), float(location["longitude"]), mode)
    except WeatherProviderError as exc:
        if use_mock_fallback:
            return _fallback_response(country, str(exc), mode)
        raise

    if mode == "current":
        records = _normalize_current_records(payload, location)
    else:
        records = [
            *_normalize_timeseries_records(payload, location, "hourly"),
            *_normalize_timeseries_records(payload, location, "daily"),
        ]

    return WeatherResponse(
        provider=settings.weather_provider,
        source_id=OPEN_METEO_SOURCE_ID,
        country=str(location["country"]),
        region=str(location["region"]),
        latitude=float(location["latitude"]),
        longitude=float(location["longitude"]),
        fallback_used=False,
        fallback_reason=None,
        records=records,
    )
