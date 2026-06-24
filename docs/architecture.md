# Architecture

The Global Risk Decision Intelligence Platform is organized as a modular application with a FastAPI backend and a React + TypeScript frontend.

## Phase Boundaries

Phase 1 creates the application foundation only.

Phase 2 adds a backend Data Source Registry for source metadata. It does not implement real data ingestion, risk scoring, alert generation, AI explanations, maps, charts, or real datasets.

## High-Level Components

- Frontend shell: displays the project name, current phase, MVP countries, MVP sectors, and backend health status.
- Backend API: exposes a minimal `/health` endpoint with structured project metadata.
- Data Source Registry API: exposes metadata endpoints under `/data-sources`.
- Configuration layer: centralizes Phase 1 constants such as app name, version, phase, local frontend origin, MVP countries, and MVP sectors.
- Database layer: uses local SQLite and SQLAlchemy for Phase 2 registry records.
- Data folders: reserve locations for future mock, raw, and processed data.
- Documentation: records architecture and MVP scope decisions before Phase 2 begins.

## Future Architecture Direction

Later phases can add these modules behind the backend API:

- Data source registry
- Mock data pipeline
- Real weather and climate integrations
- Country profile service
- Agriculture and energy risk engines
- Alert engine
- Audit and validation logs
- AI briefing generator

Each future module should keep source traceability, confidence, and rule versioning visible in its data contracts.
