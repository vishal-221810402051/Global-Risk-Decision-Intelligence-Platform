# Real Weather Data Integration

Phase 4 introduces read-only backend weather endpoints backed by Open-Meteo.

This phase does not add frontend UI, real ingestion jobs, risk scoring, alerts, predictive models, or dashboard analytics.

## Provider

The first provider is Open-Meteo Weather Forecast API:

- Base URL: `https://api.open-meteo.com/v1/forecast`
- Source ID: `open_meteo_weather`
- API key: optional for the current development integration

## MVP Locations

- India: New Delhi
- France: Paris
- Kenya: Nairobi

## Endpoints

- `GET /weather/current?country=India`
- `GET /weather/forecast?country=India`

Supported countries are India, France, and Kenya.

## Normalization

Provider responses are normalized into `WeatherRecord` objects with:

- provider
- source ID
- country and region
- latitude and longitude
- variable
- value and unit
- observed or forecast timestamp
- mock marker
- raw provider metadata

## Mock Fallback

If Open-Meteo is unavailable and mock fallback is enabled, the weather service returns Phase 3 mock weather records converted into the weather response shape.

Fallback responses are explicit:

- `fallback_used=true`
- `provider=mock_data`
- records have `is_mock=true`

The service does not silently mix real and mock weather records.
