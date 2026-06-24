from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.data_source import (
    DataSourceCreate,
    DataSourceResponse,
    DataSourceUpdate,
    DatasetType,
    Sector,
)
from app.services import data_source_service


router = APIRouter(prefix="/data-sources", tags=["data sources"])


@router.get("", response_model=list[DataSourceResponse])
def list_data_sources(
    dataset_type: DatasetType | None = None,
    sector: Sector | None = None,
    country: str | None = None,
    active_only: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> list[DataSourceResponse]:
    return data_source_service.list_data_sources(
        db=db,
        dataset_type=dataset_type.value if dataset_type else None,
        sector=sector.value if sector else None,
        country=country,
        active_only=active_only,
    )


@router.get("/{source_id}", response_model=DataSourceResponse)
def get_data_source(source_id: str, db: Session = Depends(get_db)) -> DataSourceResponse:
    data_source = data_source_service.get_data_source(db, source_id)
    if data_source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data source not found")
    return data_source


@router.post("", response_model=DataSourceResponse, status_code=status.HTTP_201_CREATED)
def create_data_source(
    data_source: DataSourceCreate,
    db: Session = Depends(get_db),
) -> DataSourceResponse:
    existing = data_source_service.get_data_source(db, data_source.source_id)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Data source already exists")

    return data_source_service.create_data_source(db, data_source)


@router.patch("/{source_id}", response_model=DataSourceResponse)
def update_data_source(
    source_id: str,
    update: DataSourceUpdate,
    db: Session = Depends(get_db),
) -> DataSourceResponse:
    data_source = data_source_service.get_data_source(db, source_id)
    if data_source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data source not found")

    return data_source_service.update_data_source(db, data_source, update)
