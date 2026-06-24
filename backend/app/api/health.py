from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings


router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    phase: str
    mvp_countries: list[str]
    mvp_sectors: list[str]


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        phase=settings.app_phase,
        mvp_countries=settings.mvp_countries,
        mvp_sectors=settings.mvp_sectors,
    )
