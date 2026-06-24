from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.data_source import DataSource
from app.schemas.data_source import DataSourceCreate, DataSourceUpdate


def list_data_sources(
    db: Session,
    dataset_type: str | None = None,
    sector: str | None = None,
    country: str | None = None,
    active_only: bool = False,
) -> list[DataSource]:
    query = select(DataSource)

    if dataset_type:
        query = query.where(DataSource.dataset_type == dataset_type)
    if sector:
        query = query.where(DataSource.sector == sector)
    if active_only:
        query = query.where(DataSource.active_flag.is_(True))

    data_sources = list(db.scalars(query).all())
    if country:
        data_sources = [source for source in data_sources if country in source.country_scope]

    return data_sources


def get_data_source(db: Session, source_id: str) -> DataSource | None:
    return db.get(DataSource, source_id)


def create_data_source(db: Session, data_source: DataSourceCreate) -> DataSource:
    db_data_source = DataSource(**data_source.model_dump(mode="json"))
    db.add(db_data_source)
    db.commit()
    db.refresh(db_data_source)
    return db_data_source


def update_data_source(db: Session, db_data_source: DataSource, update: DataSourceUpdate) -> DataSource:
    update_data = update.model_dump(exclude_unset=True, mode="json")

    for field, value in update_data.items():
        setattr(db_data_source, field, value)

    db.add(db_data_source)
    db.commit()
    db.refresh(db_data_source)
    return db_data_source
