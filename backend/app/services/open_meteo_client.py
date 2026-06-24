from typing import Any, Literal

import httpx

from app.core.config import settings


CURRENT_VARIABLES = [
    "temperature_2m",
    "apparent_temperature",
    "precipitation",
    "rain",
    "weather_code",
    "wind_speed_10m",
]

HOURLY_VARIABLES = [
    "temperature_2m",
    "precipitation",
    "rain",
    "soil_moisture_0_to_1cm",
    "soil_moisture_1_to_3cm",
]

DAILY_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "rain_sum",
]


class WeatherProviderError(Exception):
    pass


class OpenMeteoClient:
    def __init__(
        self,
        base_url: str = settings.open_meteo_base_url,
        timeout_seconds: float = settings.open_meteo_timeout_seconds,
        api_key: str = settings.open_meteo_api_key,
    ) -> None:
        self.base_url = base_url
        self.timeout_seconds = timeout_seconds
        self.api_key = api_key

    def build_request_params(
        self,
        latitude: float,
        longitude: float,
        mode: Literal["current", "forecast"],
    ) -> dict[str, str | float | int]:
        params: dict[str, str | float | int] = {
            "latitude": latitude,
            "longitude": longitude,
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm",
            "timezone": "auto",
        }

        if mode == "current":
            params["current"] = ",".join(CURRENT_VARIABLES)
        else:
            params["hourly"] = ",".join(HOURLY_VARIABLES)
            params["daily"] = ",".join(DAILY_VARIABLES)
            params["forecast_days"] = 3

        if self.api_key:
            params["apikey"] = self.api_key

        return params

    def fetch(self, latitude: float, longitude: float, mode: Literal["current", "forecast"]) -> dict[str, Any]:
        params = self.build_request_params(latitude, longitude, mode)

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.get(self.base_url, params=params)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise WeatherProviderError(f"Open-Meteo returned HTTP {exc.response.status_code}") from exc
        except httpx.RequestError as exc:
            raise WeatherProviderError("Open-Meteo request failed") from exc

        payload = response.json()
        if payload.get("error") is True:
            reason = payload.get("reason", "Unknown Open-Meteo provider error")
            raise WeatherProviderError(str(reason))

        return payload
