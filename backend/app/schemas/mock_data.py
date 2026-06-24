from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MockCountry(StrEnum):
    india = "India"
    france = "France"
    kenya = "Kenya"


class MockSector(StrEnum):
    agriculture = "Agriculture"
    energy = "Energy"
    economy = "Economy"


class CountryBaseline(BaseModel):
    model_config = ConfigDict(extra="forbid")

    country: MockCountry
    iso_code: str = Field(..., min_length=3, max_length=3)
    population_millions: float = Field(..., gt=0)
    primary_crops: list[str] = Field(..., min_length=1)
    agriculture_dependency_level: str = Field(..., min_length=1)
    energy_dependency_notes: str = Field(..., min_length=1)
    grid_stress_sensitivity: str = Field(..., min_length=1)
    climate_vulnerability_notes: str = Field(..., min_length=1)
    is_mock: bool

    @model_validator(mode="after")
    def require_mock_flag(self) -> "CountryBaseline":
        if self.is_mock is not True:
            raise ValueError("Country baseline records must be marked as mock data.")
        return self


class MockSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(..., min_length=1)
    country: MockCountry
    region: str = Field(..., min_length=1)
    sector: MockSector
    signal_type: str = Field(..., min_length=1)
    timestamp: datetime
    value: float
    unit: str = Field(..., min_length=1)
    baseline_value: float
    anomaly: float
    severity_hint: str = Field(..., min_length=1)
    source_id: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0, le=1)
    notes: str = Field(..., min_length=1)
    is_mock: bool

    @model_validator(mode="after")
    def require_mock_flag(self) -> "MockSignal":
        if self.is_mock is not True:
            raise ValueError("Signal records must be marked as mock data.")
        return self
