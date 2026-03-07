# System Architecture

## Overview

The India Patient Safety Surveillance System is designed as a federated national platform with facility, district, state, and national operational layers.

## Architectural layers

1. `Intake layer`
   - web reporting forms
   - facility safety office ingestion
   - API ingestion from HIS/EMR/LIS/RIS/claims systems
2. `Normalization layer`
   - de-duplication
   - terminology mapping
   - de-identification and privacy controls
   - severity and taxonomy mapping
3. `Case management layer`
   - triage queue
   - case ownership
   - investigation workflow
   - action and closure tracking
4. `Signal intelligence layer`
   - rule-based signal detection
   - cluster detection by geography/facility/domain
   - temporal trend analysis
   - sentinel event escalation
5. `Governance layer`
   - approval workflows
   - audit logs
   - role-based access
   - release and policy state management
6. `Analytics layer`
   - district/state/national dashboards
   - publication and policy outputs
   - benchmarking and surveillance reports
7. `Interoperability layer`
   - ABDM-compatible integration profile
   - standards mapping for FHIR, HL7, CSV, claims extracts, and manual upload workflows

## Deployment model

1. facilities report and investigate locally,
2. districts aggregate and escalate,
3. states review trends and coordinate response,
4. national node performs benchmarking, sentinel signal review, taxonomy stewardship, and publication.

## Core modules

1. reporting and intake service,
2. patient safety taxonomy service,
3. signal detection engine,
4. investigation and root-cause workflow engine,
5. governance and policy registry,
6. dashboard and publication service.
