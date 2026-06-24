from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WeatherRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    source_id: str
    country: str
    region: str
    latitude: float
    longitude: float
    variable: str
    value: float
    unit: str
    observed_at: datetime | None = None
    forecast_time: datetime | None = None
    is_mock: bool
    raw_provider_metadata: dict[str, Any] = Field(default_factory=dict)


class WeatherResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    source_id: str
    country: str
    region: str
    latitude: float
    longitude: float
    fallback_used: bool
    fallback_reason: str | None = None
    records: list[WeatherRecord]
