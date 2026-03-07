# India Patient Safety Surveillance System

## Working name

India Patient Safety Surveillance System (`IPSSS`)

## Purpose

This project defines a national-scale surveillance, signal detection, investigation, learning, and policy platform for medical errors and patient safety events in India.

It is designed to support:

1. facility-level reporting and local corrective action,
2. district and state aggregation and signal management,
3. national surveillance, benchmarking, and policy response,
4. future integration with ABDM-aligned digital health systems, hospital information systems, claims systems, pharmacovigilance, and public-health surveillance platforms.

## Operating concept

The system is designed as a federated patient safety surveillance network rather than a single centralized complaint database.

Core workflow:

`report -> triage -> classify -> detect signal -> investigate -> escalate -> learn -> govern -> publish`

## Product layers

1. reporting and intake,
2. case triage and de-identification,
3. taxonomy and risk scoring,
4. signal detection and clustering,
5. investigation and root-cause workflow,
6. action tracking and closure,
7. governance, policy, and audit,
8. analytics, publications, and public accountability.

## Repository contents

- `docs/architecture`: technical and operating architecture
- `docs/sops`: standard operating procedures
- `docs/policy`: policy, governance, and advocacy documents
- `docs/manuscripts`: publication-ready manuscript drafts and review/protocol papers
- `src/indiasurveillance`: backend API and service layer
- `frontend/india-surveillance`: web app shell
- `tests/india_surveillance`: backend validation tests

## Indian system alignment

This project is designed for future interoperability with:

1. Ayushman Bharat Digital Mission (`ABDM`),
2. Integrated Health Information Platform (`IHIP`) concepts for surveillance operations,
3. National Health Mission quality systems,
4. NABH and institutional quality/safety programs,
5. pharmacovigilance and hemovigilance programs,
6. hospital EMR/HIS, lab, radiology, and claims data sources.

## Current project state

This repository contains the end-to-end foundational package:

1. governance and architecture documents,
2. national/state/facility SOPs,
3. policy and advocacy material,
4. manuscript series and review/protocol package,
5. a functional backend/frontend scaffold with explainable demo surveillance workflows.
