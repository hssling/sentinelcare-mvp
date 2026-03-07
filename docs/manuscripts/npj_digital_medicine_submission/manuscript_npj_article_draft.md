# SentinelCare: Multidomain Patient Safety Intelligence for Real-Time Clinical Risk Control

## Abstract

Preventable harm persists across medication management, critical test-result follow-up, and deterioration recognition because safety signals remain fragmented and workflow closure is inconsistent. We developed SentinelCare, a modular patient safety intelligence platform designed for real-time event monitoring, risk detection, accountable escalation, and closed-loop review. SentinelCare integrates three pilot domains: medication safety, critical-result closure, and deterioration surveillance. The implementation combines event-driven ingestion, deterministic safety engines, multi-agent orchestration (roles A-H), role-based routing, queue-based escalation, policy lifecycle controls, and validation reporting. In demonstration runs, the system produced traceable alerts with evidence payloads, role assignment, and review-action capture while maintaining governance artifacts (policy version states and validation outputs). SentinelCare is intended as a human-in-the-loop safety layer rather than autonomous clinical decision authority. This work presents architecture and translational protocol readiness for retrospective benchmarking, silent prospective deployment, and controlled live pilot evaluation.

## Introduction

Patient safety events frequently arise from omissions, delayed responses, communication failures, and unresolved follow-up loops. Global and national safety agendas emphasize system-level controls, accountability, and learning infrastructure rather than isolated interventions. In parallel, clinical decision support and AI governance guidance increasingly require transparency, provenance, and oversight in operational deployments.

Existing tools often address narrow use-cases (for example, single-condition prediction) without integrating workflow closure, escalation ownership, and validation feedback. SentinelCare was designed to address this gap with a modular safety platform focused on near-term high-value domains: medication safety, critical-result closure, and deterioration surveillance.

This manuscript reports the conceptual and technical implementation basis for SentinelCare as a translational digital medicine system intended for staged clinical validation.

## Results

### System architecture and operational layers

SentinelCare is implemented as an event-driven, modular architecture with explicit separation of:

1. ingestion and normalization,
2. safety detection,
3. intervention routing,
4. governance and validation reporting.

Three pilot safety engines are implemented:

1. medication contraindication/dose/duplication/omission checks,
2. critical result acknowledgment and post-discharge closure checks,
3. deterioration and sepsis-bundle deviation surveillance.

### Multi-agent orchestration and traceability

The platform executes a staged multi-agent chain (A-H), where each agent contributes designated tasks to a traceable execution log:

1. scope and policy context,
2. normalization and mapping,
3. detection and safety challenge,
4. routing and escalation analysis,
5. governance and validation artifact generation.

This architecture provides explicit process observability for each event.

### Intervention workflow outputs

For triggered risks, SentinelCare generates:

1. alert type and severity,
2. evidence payload,
3. recommended action,
4. routed roles,
5. queue item with due time and escalation level.

Review actions (acknowledge, resolve, override rationale) are captured and linked back to alerts.

### Governance and validation functions

The implementation includes:

1. policy submission and approval state transitions,
2. active/inactive policy version tracking,
3. validation report generation with operational metrics (closure rate, queue status, urgency distribution).

These controls support governance-first deployment rather than model-only operation.

## Discussion

SentinelCare should be interpreted as a socio-technical safety control layer, not an autonomous clinical decision-maker. Its primary contribution is integration of detection with accountable workflow and governance artifacts in one operational loop.

The current stage emphasizes deterministic rule engines to establish high-traceability baseline behavior before broader ML integration. This is consistent with high-reliability deployment principles: introduce transparent controls first, then expand with model complexity under validation and oversight.

Key strengths include:

1. multidomain safety scope,
2. explicit human-in-the-loop closure,
3. queue and escalation operations,
4. governance and validation readiness.

Current limitations include:

1. limited live interoperability integration in the presented stage,
2. no completed prospective controlled pilot outcomes yet,
3. dependence on site-specific calibration and workflow adaptation.

Future work will focus on FHIR-native ingestion, silent prospective evaluation, and controlled pilot endpoints tied to patient-level and process-level safety outcomes.

## Methods

### Design framework

SentinelCare follows a process-chain safety model:

Intent -> Action -> Confirmation -> Response -> Follow-up -> Closure.

Risk states are encoded as omissions, contradictions, delays, or unresolved closures.

### Implementation stack

Backend services were implemented with Python/FastAPI and persisted to Supabase PostgreSQL. Frontend observability used a Netlify-hosted web console. CI/CD workflows automated testing, database migrations, and deployment pipelines.

### Safety engines

The three pilot engines use deterministic rule logic over event payloads:

1. medication safety engine,
2. critical-result closure engine,
3. deterioration surveillance engine.

Alert objects include evidence, recommended action, severity class, and role routing.

### Agent orchestration

Eight orchestration agents (A-H) execute designated task sets across foundation, detection, intervention, and governance stages. Task outputs are persisted for audit and validation reporting.

### Evaluation strategy

Validation is designed in four stages:

1. retrospective offline benchmarking,
2. silent prospective monitoring,
3. controlled live pilot,
4. scale-up assessment.

Primary metrics include alert precision, timeliness measures, closure completeness, override patterns, and operational burden metrics.

## Data availability

No patient-identifiable real-world dataset is publicly distributed in this manuscript package. Synthetic event examples and schema artifacts are included in the repository for reproducibility and simulation.

## Code availability

Project repository: https://github.com/hssling/sentinelcare-mvp

## Acknowledgements

[To be completed]

## Author contributions

[To be completed using CRediT taxonomy]

## Competing interests

The authors declare [to be completed].

## References (initial)

1. WHO Global Patient Safety Action Plan 2021-2030. https://www.who.int/publications/i/item/9789240032705
2. WHO Global Patient Safety Report 2024. https://iris.who.int/handle/10665/376928
3. National Academies. Improving Diagnosis in Health Care. https://www.nationalacademies.org/publications/21794
4. Evans L, et al. Surviving Sepsis Campaign 2021. https://pubmed.ncbi.nlm.nih.gov/34599691/
5. FDA Clinical Decision Support Software Guidance. https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software
6. FDA GMLP principles. https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles
7. ONC Decision Support Interventions transparency criteria. https://www.healthit.gov/test-method/decision-support-interventions
8. Wong A, et al. External validation of Epic Sepsis Model. JAMA Intern Med. https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307
9. Apalodimas L, et al. External validation in county EDs. https://pubmed.ncbi.nlm.nih.gov/39545248/
10. Closing-the-loop test result communication review. https://pmc.ncbi.nlm.nih.gov/articles/PMC7510293/

