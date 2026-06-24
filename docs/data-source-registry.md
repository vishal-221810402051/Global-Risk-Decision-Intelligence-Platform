# Data Source Registry

The Data Source Registry stores metadata about datasets that may be used by the Global Risk Decision Intelligence Platform.

Phase 2 is metadata-only. It does not fetch external APIs, ingest files, run transformations, score risks, or generate alerts.

## Why It Exists

The registry makes future intelligence outputs traceable. Before the platform uses a dataset, it should know where the source came from, what sector it supports, how often it refreshes, how reliable it is, and whether it is currently active.

## Registry Fields

- `source_id`: stable string primary key
- `source_name`: human-readable source name
- `source_url`: source homepage, documentation, or access URL
- `dataset_type`: one of `weather`, `climate`, `agriculture`, `energy`, `economic`, `construction`, `supply_chain`
- `sector`: one of `agriculture`, `energy`, `economy`, `construction`, `supply_chain`, `multi_sector`
- `country_scope`: list of country names covered by the source
- `refresh_frequency`: expected update cadence
- `reliability_score`: integer from 0 to 100
- `active_flag`: whether the source should be considered active
- `last_updated`: optional source freshness timestamp
- `notes`: optional context for reviewers
- `created_at`: registry record creation timestamp
- `updated_at`: registry record update timestamp

## Example Records

```json
{
  "source_id": "open_meteo_weather",
  "source_name": "Open-Meteo Weather Forecast API",
  "source_url": "https://open-meteo.com/",
  "dataset_type": "weather",
  "sector": "multi_sector",
  "country_scope": ["India", "France", "Kenya"],
  "refresh_frequency": "hourly",
  "reliability_score": 85,
  "active_flag": true,
  "last_updated": null,
  "notes": "Candidate weather source metadata only."
}
```

```json
{
  "source_id": "fao_agriculture_metadata",
  "source_name": "FAO Agriculture Dataset Metadata",
  "source_url": "https://www.fao.org/",
  "dataset_type": "agriculture",
  "sector": "agriculture",
  "country_scope": ["India", "France", "Kenya"],
  "refresh_frequency": "varies by dataset",
  "reliability_score": 90,
  "active_flag": false,
  "last_updated": null,
  "notes": "Registry candidate only; no ingestion in Phase 2."
}
```

## Traceability

Future risk scores and alerts should reference registry records by `source_id`. This keeps evidence chains auditable and helps reviewers understand which datasets influenced an operational decision.
