from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Global Risk Decision Intelligence Platform API"
    app_version: str = "0.1.0"
    app_phase: str = "Phase 3 - Mock Data Pipeline"
    frontend_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    database_url: str = "sqlite:///./grdip.db"
    mvp_countries: list[str] = ["India", "France", "Kenya"]
    mvp_sectors: list[str] = ["Agriculture", "Energy"]


settings = Settings()
