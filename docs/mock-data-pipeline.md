# Mock Data Pipeline

Phase 3 adds deterministic mock data fixtures for MVP country and sector workflows.

The mock data pipeline is intentionally read-only. It does not call real APIs, ingest live datasets, score risk, generate alerts, or power dashboard analytics.

## Purpose

The fixtures let backend contracts and future UI flows develop against stable, reviewable records before real data integration begins.

## MVP Coverage

Countries:
- India
- France
- Kenya

Sectors:
- Agriculture
- Energy

Context category:
- Economy/context signals

## Fixture Files

- `data/mock/country_baselines.json`
- `data/mock/weather_signals.json`
- `data/mock/agriculture_signals.json`
- `data/mock/energy_signals.json`
- `data/mock/economy_context_signals.json`

Every record includes `is_mock: true`.

## API Endpoints

- `GET /mock-data/countries`
- `GET /mock-data/weather`
- `GET /mock-data/agriculture`
- `GET /mock-data/energy`
- `GET /mock-data/economy-context`
- `GET /mock-data/signals`

Supported filters:

- `country`
- `sector`
- `signal_type`

## Boundaries

`severity_hint` is descriptive metadata only. It must not generate alerts or risk scores in Phase 3.

`source_id` values may look like registry IDs, but Phase 3 does not seed or mutate the Data Source Registry.
