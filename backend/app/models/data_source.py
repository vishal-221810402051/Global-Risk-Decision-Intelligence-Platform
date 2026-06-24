from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DataSource(Base):
    __tablename__ = "data_sources"

    source_id: Mapped[str] = mapped_column(String(120), primary_key=True, index=True)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str] = mapped_column(String(500), nullable=False)
    dataset_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    sector: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    country_scope: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    refresh_frequency: Mapped[str] = mapped_column(String(100), nullable=False)
    reliability_score: Mapped[int] = mapped_column(Integer, nullable=False)
    active_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
