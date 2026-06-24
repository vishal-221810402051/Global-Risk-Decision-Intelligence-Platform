from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.weather import WeatherResponse
from app.services.open_meteo_client import WeatherProviderError
from app.services.weather_service import UnsupportedCountryError, get_weather


router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/current", response_model=WeatherResponse)
def get_current_weather(country: str = Query(..., min_length=1)) -> WeatherResponse:
    try:
        return get_weather(country=country, mode="current")
    except UnsupportedCountryError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except WeatherProviderError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc


@router.get("/forecast", response_model=WeatherResponse)
def get_weather_forecast(country: str = Query(..., min_length=1)) -> WeatherResponse:
    try:
        return get_weather(country=country, mode="forecast")
    except UnsupportedCountryError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except WeatherProviderError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
