# Manuscript 01: SentinelCare Concept, Rationale, and Validation Protocol

## Working Title

SentinelCare: A Multidomain, Human-in-the-Loop Patient Safety Intelligence Platform - Conceptual Design and Staged Validation Protocol

## Target Article Type

Protocol / Methods paper (digital health, patient safety informatics)

## Abstract (Draft)

### Background

Preventable harm remains a major challenge across medication, diagnostic follow-up, and clinical deterioration pathways. Existing safety interventions are often fragmented, retrospective, and weakly integrated into real-time clinical workflow.

### Objective

To define the conceptual architecture, safety model, and staged validation protocol for SentinelCare, a patient safety intelligence platform designed for real-time detection, escalation, and closed-loop action support.

### Methods

SentinelCare combines event-driven data ingestion, deterministic safety rules, role-based alert routing, queue-based escalation, governance controls, and validation reporting. We propose four validation stages: retrospective benchmarking, silent prospective deployment, controlled live pilot, and scale-up assessment.

### Results (Protocol-level expected outputs)

Primary outputs include alert precision, sensitivity for predefined events, time-to-detection, time-to-acknowledgment, time-to-corrective-action, closure completeness, and override analysis.

### Conclusions

SentinelCare is designed as a socio-technical safety layer rather than autonomous clinical decision authority. The protocol supports transparent, governance-first deployment with measurable safety outcomes.

## Introduction (Draft)

Patient safety requires system-level observability and response, not isolated point tools. Evidence from global safety strategy and diagnostic safety literature supports closed-loop workflows with accountable action ownership. Concurrently, CDS/AI governance standards emphasize explainability, provenance, and oversight. SentinelCare addresses these needs through an integrated architecture spanning ingestion, detection, intervention, governance, and learning.

## Objectives

1. Build a platform that detects preventable safety risks in real-time.
2. Route alerts to the right role with explicit accountability and time constraints.
3. Capture review outcomes to support learning and governance.
4. Validate impact in staged deployment before broad scale-up.

## Methods

### System scope

MVP domains:

1. Medication safety
2. Critical-result closure
3. Deterioration surveillance

### Intervention model

For each event, SentinelCare executes:

1. Context and policy alignment
2. Safety detection logic
3. Alert routing and escalation
4. Queue tracking and closure capture
5. Validation and governance logging

### Outcomes and metrics

1. Alert PPV and sensitivity
2. Harmful false-positive rate
3. Time-to-detection
4. Time-to-acknowledgment
5. Time-to-action
6. Closure rate
7. Override rate and override rationale distribution

## Validation protocol (staged)

1. Retrospective offline validation
2. Silent prospective run
3. Controlled live pilot with governance board review
4. Scale-up with site adaptation and drift checks

## Ethics and governance

SentinelCare should be treated as clinical workflow support, not autonomous diagnosis/treatment authority. High-risk interventions require human confirmation. Audit trails and change-management controls are mandatory.

## Limitations

1. Early MVP emphasizes deterministic logic over advanced model learning.
2. Generalizability depends on site-specific data quality and workflow fit.
3. Prospective evidence of patient-level outcome impact is pending pilot completion.

## References (initial set)

1. WHO Global Patient Safety Action Plan 2021-2030: https://www.who.int/publications/i/item/9789240032705
2. WHO Global Patient Safety Report 2024: https://iris.who.int/handle/10665/376928
3. National Academies Improving Diagnosis in Health Care: https://www.nationalacademies.org/publications/21794
4. Surviving Sepsis Campaign 2021: https://pubmed.ncbi.nlm.nih.gov/34599691/
5. FDA CDS Guidance (2026 revision): https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software
6. ONC DSI transparency criteria: https://www.healthit.gov/test-method/decision-support-interventions

