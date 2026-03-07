# Manuscript 02: SentinelCare Architecture and Translational Implementation

## Working Title

Engineering a Multi-Agent Patient Safety Platform: Architecture, Workflow Control, and Early Translational Implementation of SentinelCare

## Target Article Type

Technical architecture / translational informatics implementation paper

## Abstract (Draft)

### Background

Real-time patient safety systems often fail when they do not align with workflow ownership, operational escalation, and governance controls.

### Objective

To describe the architecture and implementation of SentinelCare, a multi-agent, event-driven patient safety platform integrating detection, intervention, queue management, governance, and validation functions.

### Methods

A modular backend was implemented using API-driven event processing with domain safety engines, agent-orchestrated task stages, routing logic, queue escalation, policy lifecycle management, and validation report generation. A web command console supports observability across input events, analysis tasks, and outputs.

### Results

The implementation demonstrates end-to-end execution across medication, critical-result, and deterioration domains with traceable task chains and operational artifacts (alerts, queue items, review actions, policy states, validation reports).

### Conclusions

SentinelCare demonstrates architectural feasibility for governance-first real-time safety support and provides a foundation for controlled prospective evaluation.

## System architecture

### Data and event layer

1. Event ingestion API
2. Structured payload model
3. Persistence to Supabase storage

### Analysis layer

1. Deterministic safety engines (3 domains)
2. Agent A-H stage orchestration
3. Alert generation with evidence and severity tags

### Intervention and operations layer

1. Role-based routing
2. Workflow queue with due times and escalation levels
3. Human review action capture and closure status

### Governance and validation layer

1. Policy version submission/approval lifecycle
2. Validation report generation with operational metrics
3. Audit-ready traces and summary metrics

## Implementation details

### Agent design

Agents are software execution roles, each with designated tasks:

1. A-C: context and data readiness
2. D-E: detection and safety challenge
3. F: intervention routing
4. G-H: governance and validation artifacts

### API capabilities

1. Event processing and demo capability runs
2. Agent catalog and per-agent execution
3. Queue listing and escalation
4. Governance policy submit/approve/list
5. Validation report create/list

### Deployment model

1. Netlify frontend deployment
2. Supabase schema migrations and storage
3. API container build pipeline

## Comparative positioning vs existing systems

1. Unlike single-model sepsis tools, SentinelCare is multimodule and multidomain.
2. Unlike dashboard-only systems, it includes queue/escalation operations.
3. Unlike opaque CDS logic, it emphasizes explicit evidence and task traceability.
4. Unlike pure model-centric pipelines, it embeds governance endpoints and policy states in core architecture.

## Discussion

SentinelCare is not a finished clinical product. It is a translational scaffold intended to support rigorous pilot design. Its main contribution is socio-technical integration: analysis plus accountable workflow plus governance.

## Future work

1. FHIR-native ingestion
2. Prospective silent-mode trial and calibration
3. Drift/fairness monitoring
4. Role-based authentication and production-grade security controls
5. Multi-site adaptation framework

## References (initial set)

1. Epic sepsis model external validation: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307
2. External county ED validation (JAMIA Open): https://pubmed.ncbi.nlm.nih.gov/39545248/
3. Real-time ML sepsis alert trial: https://pubmed.ncbi.nlm.nih.gov/38381351/
4. Critical result loop closure review: https://pmc.ncbi.nlm.nih.gov/articles/PMC7510293/
5. FDA GMLP principles: https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles

