import json
from functools import lru_cache
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, TypeAdapter

from app.schemas.mock_data import CountryBaseline, MockSignal


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MOCK_DATA_DIR = PROJECT_ROOT / "data" / "mock"

T = TypeVar("T", bound=BaseModel)


def _load_json_file(file_name: str) -> object:
    with (MOCK_DATA_DIR / file_name).open(encoding="utf-8") as fixture_file:
        return json.load(fixture_file)


def _load_records(file_name: str, model: type[T]) -> list[T]:
    adapter = TypeAdapter(list[model])
    return adapter.validate_python(_load_json_file(file_name))


def _normalize_filter(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip().casefold()


def _matches_filter(record_value: str, filter_value: str | None) -> bool:
    normalized_filter = _normalize_filter(filter_value)
    if normalized_filter is None:
        return True
    return record_value.casefold() == normalized_filter


def _filter_signals(
    signals: list[MockSignal],
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = None,
) -> list[MockSignal]:
    return [
        signal
        for signal in signals
        if _matches_filter(signal.country, country)
        and _matches_filter(signal.sector, sector)
        and _matches_filter(signal.signal_type, signal_type)
    ]


@lru_cache
def get_country_baselines() -> list[CountryBaseline]:
    return _load_records("country_baselines.json", CountryBaseline)


@lru_cache
def get_weather_signals() -> list[MockSignal]:
    return _load_records("weather_signals.json", MockSignal)


@lru_cache
def get_agriculture_signals() -> list[MockSignal]:
    return _load_records("agriculture_signals.json", MockSignal)


@lru_cache
def get_energy_signals() -> list[MockSignal]:
    return _load_records("energy_signals.json", MockSignal)


@lru_cache
def get_economy_context_signals() -> list[MockSignal]:
    return _load_records("economy_context_signals.json", MockSignal)


def list_country_baselines(country: str | None = None) -> list[CountryBaseline]:
    return [baseline for baseline in get_country_baselines() if _matches_filter(baseline.country, country)]


def list_weather_signals(
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = None,
) -> list[MockSignal]:
    return _filter_signals(get_weather_signals(), country, sector, signal_type)


def list_agriculture_signals(
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = None,
) -> list[MockSignal]:
    return _filter_signals(get_agriculture_signals(), country, sector, signal_type)


def list_energy_signals(
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = None,
) -> list[MockSignal]:
    return _filter_signals(get_energy_signals(), country, sector, signal_type)


def list_economy_context_signals(
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = None,
) -> list[MockSignal]:
    return _filter_signals(get_economy_context_signals(), country, sector, signal_type)


def list_all_signals(
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = None,
) -> list[MockSignal]:
    signals = [
        *get_weather_signals(),
        *get_agriculture_signals(),
        *get_energy_signals(),
        *get_economy_context_signals(),
    ]
    return _filter_signals(signals, country, sector, signal_type)
