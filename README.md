# SentinelCare

SentinelCare is a multi-agent patient safety platform focused on preventing medical errors through real-time detection, risk surveillance, intervention routing, and auditable human review.

## Vision

Build an always-on safety copilot that monitors workflows, detects harmful deviations early, and helps clinical teams take safer actions with full traceability.

See:
- [Vision](/d:/Medical%20Error%20U-HEDPPLS/docs/vision.md)
- [Architecture](/d:/Medical%20Error%20U-HEDPPLS/docs/multi_agent_architecture.md)
- [Workflows](/d:/Medical%20Error%20U-HEDPPLS/docs/workflows.md)
- [CI/CD and Automation](/d:/Medical%20Error%20U-HEDPPLS/docs/cicd.md)
- [Netlify + Supabase Deployment](/d:/Medical%20Error%20U-HEDPPLS/docs/deployment_netlify_supabase.md)
- [Roadmap](/d:/Medical%20Error%20U-HEDPPLS/docs/roadmap.md)
- [IDE to Production Automation](/d:/Medical%20Error%20U-HEDPPLS/docs/ide_to_prod_automation.md)

## Stack

- Backend: Python, FastAPI, Pydantic
- Frontend: React + Vite (Netlify-hosted)
- Data: Supabase Postgres
- Automation: GitHub Actions CI/CD
- Container: Docker image for API (GHCR)

## What These Agents Are

- They are orchestrated software roles (A-H) that execute designated pipeline tasks.
- They are not autonomous clinical decision-makers.
- They are not all separately "trained models". Current MVP uses deterministic safety logic and orchestrated workflow stages.
- ML model integration is planned for temporal risk and advanced prediction modules.

## End-to-end flow

1. Event arrives (API or synthetic runner).
2. Agent A-H orchestration executes scope, normalization, detection, routing, audit, validation.
3. Alerts are generated for:
   - medication safety
   - critical-result closure
   - deterioration surveillance
4. Alerts are routed to role-specific recipients.
5. Human review action closes/overrides alerts.
6. Events, alerts, tasks, and review actions persist to Supabase when credentials are configured.
7. Agent execution traces are logged with per-agent task counts.

Operational endpoint:
- `GET /metrics/summary`
- `GET /agents/catalog`
- `POST /agents/run`
- `GET /demo/scenarios`
- `POST /demo/capability-run`

## Local development

### Backend

```bash
python -m pip install -e .[dev]
python -m pytest -q
sentinelcare-demo
sentinelcare-api
```

Capability demo from API:

```bash
curl -X POST http://localhost:8000/demo/capability-run
```

### Frontend

```bash
cd frontend/web
npm install
npm run dev
```

## Environment

Copy `.env.example` to `.env` and set:

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

## GitHub Actions workflows

- `.github/workflows/ci.yml`: backend test + frontend build
- `.github/workflows/deploy-netlify.yml`: production deploy to Netlify on `main`
- `.github/workflows/supabase-db.yml`: migration push to Supabase on `main`
- `.github/workflows/deploy-api-image.yml`: build/push API image to GHCR

## Repository layout

- `src/sentinelcare`: API, pipeline, domain engines, agents, Supabase persistence
- `frontend/web`: Netlify UI connected to Supabase
- `supabase/migrations`: database schema migrations
- `docs`: product and engineering documentation
- `.github/workflows`: CI/CD pipelines
