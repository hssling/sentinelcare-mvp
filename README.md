# Medical Error and Patient Safety Systems

This repository contains two related product lines built around clinical safety detection, surveillance, learning, and governance:

1. `SentinelCare`
2. `India Patient Safety Surveillance System`

The repo is not a single toy app. It is a working research-and-product workspace that combines:

- multi-agent safety workflow orchestration
- operational web applications
- Supabase-backed persistence
- GitHub Actions CI/CD
- deployment automation
- technical documentation
- policy and advocacy material
- publication-oriented manuscript packages

## Repository Scope

### 1. SentinelCare

SentinelCare is the prospective safety intelligence layer.

Its purpose is to detect workflow deviations and high-risk safety conditions early, route interventions, and preserve full traceability for review and governance.

Current implemented direction includes:

- multi-agent orchestration (`A-H`)
- detection engines for medication, critical-result, and deterioration workflows
- workflow queue and escalation logic
- governance and validation scaffolding
- Supabase-backed storage
- frontend command console
- manuscript and architecture documentation

Primary code locations:

- [src/sentinelcare](d:/Medical%20Error%20U-HEDPPLS/src/sentinelcare)
- [frontend/web](d:/Medical%20Error%20U-HEDPPLS/frontend/web)
- [docs](d:/Medical%20Error%20U-HEDPPLS/docs)

### 2. India Patient Safety Surveillance System

This is the federated manual-plus-digital surveillance layer intended for facility, state, and national workflows in India.

Its purpose is to support:

- department-level daily surveillance submission
- event-level case intake and review
- state/national signal aggregation
- audit, policy, and governance review
- trend analytics
- AI-assisted case support
- eventual integration with SentinelCare and national digital health systems

Primary code locations:

- [src/indiasurveillance](d:/Medical%20Error%20U-HEDPPLS/src/indiasurveillance)
- [frontend/india-surveillance](d:/Medical%20Error%20U-HEDPPLS/frontend/india-surveillance)
- [projects/india_patient_safety_surveillance](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance)

## How The Two Systems Fit Together

The intended platform model is layered:

1. `SentinelCare` handles prospective workflow intelligence from clinical and operational event streams.
2. `India Patient Safety Surveillance System` handles manual reporting, review, learning, aggregation, and governance.
3. Both should converge into a unified safety-event model over time.

In practical terms:

- SentinelCare can generate reviewed signal candidates and machine-detected case records.
- India surveillance can collect daily denominators, manual event cases, CAPA, and governance actions.
- The surveillance layer then becomes the learning and policy feedback layer for the detection layer.

## Concept and Creation Credit

The core concept, founder blueprint, and manuscript-linked intellectual framing for this repository originate from:

- `Dr Siddalingaiah H S`
- `Professor, Community Medicine`
- `Shridevi Institute of Medical Sciences and Research Hospital, Tumkur`
- `ORCID: 0000-0002-4771-8285`

This repository contains implementation, documentation, manuscript packaging, and deployment work built around that originating conceptual framework.

Primary source artifacts in the repository include:

- [Project Sentinel Care Founder Blueprint1.docx](d:/Medical%20Error%20U-HEDPPLS/Project%20Sentinel%20Care%20Founder%20Blueprint1.docx)
- [Project Sentinel Care Founder Blueprint1.pdf](d:/Medical%20Error%20U-HEDPPLS/Project%20Sentinel%20Care%20Founder%20Blueprint1.pdf)
- [project_sentinel_care_founder_blueprint1.md](d:/Medical%20Error%20U-HEDPPLS/project_sentinel_care_founder_blueprint1.md)

## Current Live Surfaces

### India surveillance

- Frontend: `https://mederror-india-surveillance.netlify.app/`
- API: `http://13.60.51.34:8010`
- Health: `http://13.60.51.34:8010/health`

### SentinelCare

- Frontend: `https://sentinelcare-mvp.netlify.app/`
- Repository: `https://github.com/hssling/sentinelcare-mvp`

## Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- JWT auth
- Supabase Python client

### Frontend

- React
- Vite
- PWA support on India surveillance frontend

### Data and persistence

- Supabase Postgres
- migration-driven schema management

### Automation

- GitHub Actions CI
- Netlify deploy workflows
- Supabase migration workflows
- VM deploy workflows

## Top-Level Layout

- [src](d:/Medical%20Error%20U-HEDPPLS/src): backend application code
- [frontend](d:/Medical%20Error%20U-HEDPPLS/frontend): web applications
- [docs](d:/Medical%20Error%20U-HEDPPLS/docs): SentinelCare product, research, and manuscript documentation
- [projects](d:/Medical%20Error%20U-HEDPPLS/projects): project-specific packages, especially India surveillance
- [supabase](d:/Medical%20Error%20U-HEDPPLS/supabase): SentinelCare Supabase migrations
- [tests](d:/Medical%20Error%20U-HEDPPLS/tests): test suites
- [.github/workflows](d:/Medical%20Error%20U-HEDPPLS/.github/workflows): CI/CD definitions

## Quick Start

### Python environment

```bash
python -m pip install -e .[dev]
pytest -q
```

### SentinelCare local

```bash
sentinelcare-api
sentinelcare-demo
```

### India surveillance local API

```bash
india-surveillance-api
```

### Frontend development

SentinelCare:

```bash
cd frontend/web
npm install
npm run dev
```

India surveillance:

```bash
cd frontend/india-surveillance
npm install
npm run dev
```

## Environment Configuration

Use [.env.example](d:/Medical%20Error%20U-HEDPPLS/.env.example) as the base.

Important environment families in this repo:

- SentinelCare:
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `VITE_SUPABASE_URL`
  - `VITE_SUPABASE_ANON_KEY`
  - `VITE_API_BASE_URL`

- India surveillance:
  - `SUPABASE_INDIA_URL`
  - `SUPABASE_INDIA_SERVICE_ROLE_KEY`
  - `SUPABASE_INDIA_ANON_KEY`
  - `INDIA_SURVEILLANCE_JWT_SECRET`
  - `VITE_INDIA_SURVEILLANCE_API_BASE`

## CI/CD Workflows

Core workflows in [.github/workflows](d:/Medical%20Error%20U-HEDPPLS/.github/workflows):

- `ci.yml`
- `deploy-netlify.yml`
- `supabase-db.yml`
- `deploy-api-image.yml`
- `india-surveillance-ci.yml`
- `deploy-india-surveillance-netlify.yml`
- `india-surveillance-supabase-db.yml`
- `deploy-india-surveillance-api-vm.yml`

## Documentation Index

### SentinelCare documentation

Architecture and product:

- [Vision](d:/Medical%20Error%20U-HEDPPLS/docs/vision.md)
- [Multi-Agent Architecture](d:/Medical%20Error%20U-HEDPPLS/docs/multi_agent_architecture.md)
- [Workflows](d:/Medical%20Error%20U-HEDPPLS/docs/workflows.md)
- [CI/CD](d:/Medical%20Error%20U-HEDPPLS/docs/cicd.md)
- [Deployment](d:/Medical%20Error%20U-HEDPPLS/docs/deployment_netlify_supabase.md)
- [Roadmap](d:/Medical%20Error%20U-HEDPPLS/docs/roadmap.md)
- [IDE to Production Automation](d:/Medical%20Error%20U-HEDPPLS/docs/ide_to_prod_automation.md)

Research and manuscripts:

- [Literature Landscape](d:/Medical%20Error%20U-HEDPPLS/docs/research/literature_landscape.md)
- [Guideline Alignment Matrix](d:/Medical%20Error%20U-HEDPPLS/docs/research/guideline_alignment_matrix.md)
- [Theoretical Framework](d:/Medical%20Error%20U-HEDPPLS/docs/research/theoretical_framework.md)
- [Stepwise Build Plan](d:/Medical%20Error%20U-HEDPPLS/docs/research/stepwise_build_plan.md)
- [Target Journal Packages](d:/Medical%20Error%20U-HEDPPLS/docs/manuscripts/target_journal_packages)

### India surveillance documentation

Project entrypoint:

- [Project README](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/README.md)

Architecture:

- [Vision and Scope](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/vision_and_scope.md)
- [System Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/system_architecture.md)
- [Data and Integration Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/data_and_integration_architecture.md)
- [Governance and Operating Model](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/governance_and_operating_model.md)
- [National Minimum Dataset](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/national_minimum_dataset.md)
- [Unified Manual and SentinelCare Ingestion](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/unified_manual_and_sentinelcare_ingestion.md)
- [AI-Assisted Workflow Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/ai_assisted_workflow_architecture.md)

Operations, policy, and deployment:

- [SOPs](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/sops)
- [Policy Documents](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/policy)
- [Deployment Guides](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/deployment)
- [Running the Prototype](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/running_the_prototype.md)

Publication assets:

- [India Manuscripts](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts)
- [India Target Journal Packages](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/target_journal_packages)

## Product Maturity

This repository contains working systems, but not all parts are at the same maturity level.

### Strongly implemented

- frontend and backend scaffolds
- Supabase-backed persistence
- authentication and role-aware flows
- deployment automation
- architecture and manuscript foundation
- live India surveillance deployment path

### Still evolving

- full SentinelCare production-grade clinical integration
- stable live `event_cases` seeding on India surveillance in all environments
- route-level frontend decomposition beyond the current view-based structure
- richer analytics and operational benchmarking
- mature multi-site production operations

## Intended Users

- clinicians
- facility safety officers
- district and state surveillance analysts
- national safety/governance teams
- informatics researchers
- quality improvement leaders
- digital health architects

## Research and Publication Intent

This repo is also a manuscript and framework workspace.

It includes:

- theoretical frameworks
- full-length IMRAD manuscripts
- journal-targeted submission packages
- review/protocol papers
- policy briefs and advocacy documents

The repository is intended to support both product development and scholarly output.

## Practical Start Points

If you are reading this repo for the first time:

1. start with [projects/india_patient_safety_surveillance/README.md](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/README.md) if your focus is national surveillance
2. start with [docs/vision.md](d:/Medical%20Error%20U-HEDPPLS/docs/vision.md) and [docs/multi_agent_architecture.md](d:/Medical%20Error%20U-HEDPPLS/docs/multi_agent_architecture.md) if your focus is SentinelCare
3. inspect [.github/workflows](d:/Medical%20Error%20U-HEDPPLS/.github/workflows) if your focus is deployment and automation
4. inspect [src](d:/Medical%20Error%20U-HEDPPLS/src) and [frontend](d:/Medical%20Error%20U-HEDPPLS/frontend) if your focus is implementation
