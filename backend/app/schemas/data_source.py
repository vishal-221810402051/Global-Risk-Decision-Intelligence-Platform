from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class DatasetType(StrEnum):
    weather = "weather"
    climate = "climate"
    agriculture = "agriculture"
    energy = "energy"
    economic = "economic"
    construction = "construction"
    supply_chain = "supply_chain"


class Sector(StrEnum):
    agriculture = "agriculture"
    energy = "energy"
    economy = "economy"
    construction = "construction"
    supply_chain = "supply_chain"
    multi_sector = "multi_sector"


class DataSourceBase(BaseModel):
    source_name: str = Field(..., min_length=1, max_length=255)
    source_url: str = Field(..., min_length=1, max_length=500)
    dataset_type: DatasetType
    sector: Sector
    country_scope: list[str] = Field(..., min_length=1)
    refresh_frequency: str = Field(..., min_length=1, max_length=100)
    reliability_score: int = Field(..., ge=0, le=100)
    active_flag: bool = True
    last_updated: datetime | None = None
    notes: str | None = None


class DataSourceCreate(DataSourceBase):
    source_id: str = Field(..., min_length=1, max_length=120, pattern=r"^[a-z0-9][a-z0-9_-]*$")


class DataSourceUpdate(BaseModel):
    source_name: str | None = Field(default=None, min_length=1, max_length=255)
    source_url: str | None = Field(default=None, min_length=1, max_length=500)
    dataset_type: DatasetType | None = None
    sector: Sector | None = None
    country_scope: list[str] | None = Field(default=None, min_length=1)
    refresh_frequency: str | None = Field(default=None, min_length=1, max_length=100)
    reliability_score: int | None = Field(default=None, ge=0, le=100)
    active_flag: bool | None = None
    last_updated: datetime | None = None
    notes: str | None = None


class DataSourceResponse(DataSourceBase):
    model_config = ConfigDict(from_attributes=True)

    source_id: str
    created_at: datetime
    updated_at: datetime
