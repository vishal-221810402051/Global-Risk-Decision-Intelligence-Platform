# Global Risk Decision Intelligence Platform

An AI decision-intelligence platform that converts climate, economic, agriculture, energy, construction, and supply-chain signals into early operational alerts.

Phase 1 creates the base application foundation only: a FastAPI backend, a React + TypeScript + Vite frontend, environment examples, documentation, and a simple health contract.

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
- Frontend: React, TypeScript, Vite
- Testing: Pytest for backend
- Data foundation: local `data/` folders only in Phase 1

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

Phase 1 does not include data ingestion, data source registry, risk scoring, real datasets, dashboard analytics, maps, or charts.
