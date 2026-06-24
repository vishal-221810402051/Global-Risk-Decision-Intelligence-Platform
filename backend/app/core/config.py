from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Global Risk Decision Intelligence Platform API"
    app_version: str = "0.1.0"
    app_phase: str = "Phase 4 - Real Weather Data Integration"
    frontend_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    database_url: str = "sqlite:///./grdip.db"
    weather_provider: str = "open_meteo"
    open_meteo_base_url: str = "https://api.open-meteo.com/v1/forecast"
    open_meteo_timeout_seconds: float = 10
    open_meteo_use_mock_fallback: bool = True
    open_meteo_api_key: str = ""
    mvp_countries: list[str] = ["India", "France", "Kenya"]
    mvp_sectors: list[str] = ["Agriculture", "Energy"]


settings = Settings()
