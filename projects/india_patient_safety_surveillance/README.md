# India Patient Safety Surveillance System

This project defines the architecture, operating model, product scaffold, and publication package for a federated patient safety surveillance system in India.

It is designed for facility, district, state, and national use.

## Purpose

The system is intended to support:

1. daily department-level surveillance
2. event-level case intake and investigation
3. facility and state review workflows
4. signal detection and escalation
5. corrective and preventive action (`CAPA`) tracking
6. trend analytics and benchmarking
7. governance, audit, and policy review
8. future interoperability with national and institutional digital health systems

This is not framed as a complaint portal. It is framed as an operational surveillance and learning system.

## Core Workflow

`submit -> review -> classify -> investigate -> escalate -> act -> learn -> govern`

The project is intended to support both:

- routine burden surveillance
- deeper event-case learning workflows

## What Exists In This Project

### Functional application scaffold

Backend:

- role-based login and JWT auth
- facilities, departments, users, daily submissions
- event reports and event cases
- notifications and audit logs
- AI provider configuration and AI-assist workflow
- trend and dashboard endpoints

Frontend:

- operational login experience
- route-oriented view model:
  - dashboard
  - submissions
  - cases
  - AI
  - governance
- responsive design
- PWA support

### Operating and policy package

- architecture documents
- SOPs
- governance and advocacy documents
- deployment and automation guides

### Research package

- manuscripts
- review article draft
- systematic review/meta-analysis protocol
- journal-targeted submission packages

Current IJMR-targeted packages:

- [Federated surveillance framework package](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/target_journal_packages/ijmr_special_article_surveillance/README.md)
- [Reporting and learning systems review package](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/target_journal_packages/ijmr_review_patient_safety_learning_systems/README.md)
- [Governance and bounded AI package](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/target_journal_packages/ijmr_governance_bounded_ai_safety_surveillance/README.md)

Supporting IJMR decision assets:

- [IJMR submission priority note](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/target_journal_packages/ijmr_submission_priority_note.md)
- [IJMR lead-package submission checklist](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/target_journal_packages/ijmr_submission_checklist_lead_package.md)
- [IJMR round-1 frozen submission candidate](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/target_journal_packages/ijmr_submission_candidate_round1/README.md)

## Code Locations

- backend: [src/indiasurveillance](d:/Medical%20Error%20U-HEDPPLS/src/indiasurveillance)
- frontend: [frontend/india-surveillance](d:/Medical%20Error%20U-HEDPPLS/frontend/india-surveillance)
- tests: [tests/india_surveillance](d:/Medical%20Error%20U-HEDPPLS/tests/india_surveillance)
- migrations: [supabase/migrations](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/supabase/migrations)

## Live Deployment

- frontend: `https://mederror-india-surveillance.netlify.app/`
- API: `http://13.60.51.34:8010`
- health: `http://13.60.51.34:8010/health`

## Current Role Model

Implemented roles include:

- `facility_reporter`
- `facility_safety_officer`
- `district_reviewer`
- `state_cell_analyst`
- `national_analyst`
- `governance_admin`

These roles are used to control:

- data entry
- review access
- case triage and closure
- user management
- governance visibility

## Data Model Direction

The system intentionally separates:

1. `daily operational surveillance`
2. `event-level learning cases`

This is critical because daily burden tracking and case investigation are not the same workflow.

Current model areas include:

- facilities
- departments
- users
- daily submissions
- event reports
- event cases
- notifications
- audit logs
- AI provider configurations

Architecture references:

- [National Minimum Dataset](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/national_minimum_dataset.md)
- [Unified Manual and SentinelCare Ingestion](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/unified_manual_and_sentinelcare_ingestion.md)
- [AI-Assisted Workflow Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/ai_assisted_workflow_architecture.md)

## National-Scale Design Intent

The system is being designed for national-scale learning and prevention, not only local reporting.

That means the intended mature system should support:

- facility-level daily denominators
- event-level case review
- comparable taxonomy
- state-cell aggregation
- signal escalation
- policy feedback loops
- benchmark reporting
- integration with prospective safety systems such as SentinelCare

## Interoperability Direction

The architecture is aligned for future interoperability with:

- ABDM-aligned registries and digital identifiers
- hospital EMR/HIS systems
- lab and radiology systems
- pharmacovigilance / materiovigilance style workflows
- public-health surveillance operating concepts
- SentinelCare prospective safety intelligence

Related references:

- [System Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/system_architecture.md)
- [Data and Integration Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/data_and_integration_architecture.md)
- [Governance and Operating Model](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/governance_and_operating_model.md)

## AI Integration

The project already supports user-side AI provider configuration and AI-assisted workflow hooks.

Implemented provider support includes:

- OpenAI
- Anthropic
- Google AI Studio / Gemini
- OpenRouter
- Groq
- Together AI
- Cohere
- xAI

AI is intended as a bounded assistance layer for:

- narrative structuring
- case classification
- severity and taxonomy suggestion
- clustering and summarization
- CAPA drafting support

AI is not intended to replace human accountability for serious event review.

## How To Run

### Backend

From repository root:

```bash
python -m pip install -e .[dev]
india-surveillance-api
```

### Frontend

```bash
cd frontend/india-surveillance
npm install
npm run dev
```

### Tests

```bash
pytest tests/india_surveillance -q
```

## Required Environment Variables

Important backend variables:

- `SUPABASE_INDIA_URL`
- `SUPABASE_INDIA_SERVICE_ROLE_KEY`
- `INDIA_SURVEILLANCE_JWT_SECRET`

Frontend/runtime variable:

- `VITE_INDIA_SURVEILLANCE_API_BASE`

## Deployment and Automation

Deployment documents:

- [Deployment and Automation](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/deployment/deployment_and_automation.md)
- [Render Setup](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/deployment/render_setup.md)
- [VM Setup](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/deployment/vm_setup.md)

Related workflows:

- [india-surveillance-ci.yml](d:/Medical%20Error%20U-HEDPPLS/.github/workflows/india-surveillance-ci.yml)
- [deploy-india-surveillance-netlify.yml](d:/Medical%20Error%20U-HEDPPLS/.github/workflows/deploy-india-surveillance-netlify.yml)
- [india-surveillance-supabase-db.yml](d:/Medical%20Error%20U-HEDPPLS/.github/workflows/india-surveillance-supabase-db.yml)
- [deploy-india-surveillance-api-vm.yml](d:/Medical%20Error%20U-HEDPPLS/.github/workflows/deploy-india-surveillance-api-vm.yml)

## Documentation Guide

### Architecture

- [Vision and Scope](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/vision_and_scope.md)
- [System Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/system_architecture.md)
- [Data and Integration Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/data_and_integration_architecture.md)
- [Governance and Operating Model](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/governance_and_operating_model.md)
- [National Minimum Dataset](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/national_minimum_dataset.md)
- [Unified Manual and SentinelCare Ingestion](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/unified_manual_and_sentinelcare_ingestion.md)
- [AI-Assisted Workflow Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/ai_assisted_workflow_architecture.md)

### SOPs

- [National Operations SOP](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/sops/national_operations_sop.md)
- [State Surveillance Cell SOP](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/sops/state_surveillance_cell_sop.md)
- [Facility Reporting SOP](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/sops/facility_reporting_sop.md)
- [Signal Detection and Investigation SOP](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/sops/signal_detection_and_investigation_sop.md)

### Policy and governance

- [Policy Brief](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/policy/policy_brief.md)
- [Advocacy Memo](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/policy/advocacy_memo.md)
- [Legal and Regulatory Alignment](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/policy/legal_and_regulatory_alignment.md)

### Manuscripts

- [Manuscript 1: National Framework](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/manuscript_1_national_framework.md)
- [Manuscript 2: Architecture and Implementation](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/manuscript_2_architecture_and_implementation.md)
- [Manuscript 3: Governance and Ethics](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/manuscript_3_governance_and_ethics.md)
- [Review Article](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/review_article_india_patient_safety_landscape.md)
- [Systematic Review / Meta-Analysis Protocol](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/systematic_review_meta_analysis_protocol.md)
- [Target Journal Packages](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/target_journal_packages)
- [IJMR Special Article Package](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/manuscripts/target_journal_packages/ijmr_special_article_surveillance/README.md)

## Current Maturity

### Working now

- role-based login
- live frontend and API
- dashboard and trend views
- daily surveillance submission workflow
- event-case creation and review workflow
- notifications and audit trail scaffolding
- AI provider configuration path
- VM and Netlify deployment automation

### Still maturing

- stable live seeding and use of `event_cases` in all environments
- more advanced benchmarking and cohort analytics
- dedicated route-level React pages instead of view switching inside a single file
- full integration with prospective clinical detection systems

## Recommended Reading Order

If you are new to the project:

1. read [Vision and Scope](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/vision_and_scope.md)
2. read [System Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/system_architecture.md)
3. read [National Minimum Dataset](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/national_minimum_dataset.md)
4. read [AI-Assisted Workflow Architecture](d:/Medical%20Error%20U-HEDPPLS/projects/india_patient_safety_surveillance/docs/architecture/ai_assisted_workflow_architecture.md)
5. then inspect the live app and code
