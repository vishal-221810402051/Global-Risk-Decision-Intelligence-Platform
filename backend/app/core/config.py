from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Global Risk Decision Intelligence Platform API"
    app_version: str = "0.1.0"
    app_phase: str = "Phase 1 - Base App Setup"
    frontend_origin: str = "http://localhost:5173"
    mvp_countries: list[str] = ["India", "France", "Kenya"]
    mvp_sectors: list[str] = ["Agriculture", "Energy"]


settings = Settings()
