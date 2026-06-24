from fastapi import APIRouter, Query

from app.schemas.mock_data import CountryBaseline, MockSignal
from app.services import mock_data_service


router = APIRouter(prefix="/mock-data", tags=["mock data"])


@router.get("/countries", response_model=list[CountryBaseline])
def list_country_baselines(country: str | None = None) -> list[CountryBaseline]:
    return mock_data_service.list_country_baselines(country=country)


@router.get("/weather", response_model=list[MockSignal])
def list_weather_signals(
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = Query(default=None),
) -> list[MockSignal]:
    return mock_data_service.list_weather_signals(country, sector, signal_type)


@router.get("/agriculture", response_model=list[MockSignal])
def list_agriculture_signals(
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = Query(default=None),
) -> list[MockSignal]:
    return mock_data_service.list_agriculture_signals(country, sector, signal_type)


@router.get("/energy", response_model=list[MockSignal])
def list_energy_signals(
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = Query(default=None),
) -> list[MockSignal]:
    return mock_data_service.list_energy_signals(country, sector, signal_type)


@router.get("/economy-context", response_model=list[MockSignal])
def list_economy_context_signals(
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = Query(default=None),
) -> list[MockSignal]:
    return mock_data_service.list_economy_context_signals(country, sector, signal_type)


@router.get("/signals", response_model=list[MockSignal])
def list_all_signals(
    country: str | None = None,
    sector: str | None = None,
    signal_type: str | None = Query(default=None),
) -> list[MockSignal]:
    return mock_data_service.list_all_signals(country, sector, signal_type)
