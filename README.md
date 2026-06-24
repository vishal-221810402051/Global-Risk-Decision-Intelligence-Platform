# Global Risk Decision Intelligence Platform

An AI decision-intelligence platform that converts climate, economic, agriculture, energy, construction, and supply-chain signals into early operational alerts.

Phase 1 created the base application foundation: a FastAPI backend, a React + TypeScript + Vite frontend, environment examples, documentation, and a simple health contract.

Phase 2 adds a backend Data Source Registry for dataset metadata and traceability. It does not ingest real data or generate alerts.

Phase 3 adds deterministic mock data fixtures and read-only backend APIs for MVP country and sector signals. It does not call real APIs, score risks, generate alerts, or add dashboard analytics.

## MVP Scope

Countries:
- India
- France
- Kenya

Sectors:
- Agriculture
- Energy

Initial alerts:
- Drought risk
- Crop stress
- Heatwave/grid stress

## Tech Stack

- Backend: Python, FastAPI, Pydantic, Uvicorn
- Database: SQLite with SQLAlchemy
- Frontend: React, TypeScript, Vite
- Testing: Pytest for backend
- Data foundation: local `data/` folders only in Phase 1

## Backend API

- `GET /health`
- `GET /data-sources`
- `GET /data-sources/{source_id}`
- `POST /data-sources`
- `PATCH /data-sources/{source_id}`
- `GET /mock-data/countries`
- `GET /mock-data/weather`
- `GET /mock-data/agriculture`
- `GET /mock-data/energy`
- `GET /mock-data/economy-context`
- `GET /mock-data/signals`

There is no `DELETE` endpoint in Phase 2. Set `active_flag` to `false` to deactivate a source.

## Setup

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Backend tests:

```bash
cd backend
pytest
```

## Phase Workflow

Every phase follows:

1. Diagnosis / Investigation
2. Implementation
3. Validation
4. Git commit and push
5. Next phase lock

Phase 3 does not include real data ingestion, risk scoring, real datasets, dashboard analytics, maps, charts, or alert generation.
