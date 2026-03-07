# Unified Manual and SentinelCare Ingestion Model

## Objective

The India surveillance system and the earlier SentinelCare platform should not remain separate products.

They should be connected as two layers of one surveillance and intervention ecosystem:

1. `India surveillance platform`
   - manual reporting
   - administrative review
   - district/state/national aggregation
   - governance and policy outputs
2. `SentinelCare`
   - live clinical workflow intelligence
   - multi-agent safety detection
   - explainable traces
   - intervention support

## Core integration principle

All incoming information should land in one canonical `safety event` model regardless of source.

Source systems become input modes, not separate data silos.

## Input modes

### 1. Manual daily operational feed

Submitted by departments and facilities:

1. daily surveillance burden
2. denominator counts
3. escalation flags
4. narrative notes

This is the `human-entered operational stream`.

### 2. Manual event-level case entry

Submitted by safety officers or investigators:

1. detailed incident record
2. contributing factors
3. immediate containment
4. investigation and CAPA details

This is the `human-entered case stream`.

### 3. SentinelCare machine-detected case stream

Produced by the earlier agent architecture:

1. medication safety contradictions
2. critical result closure failures
3. deterioration and escalation failures
4. routed alerts and traces
5. human review actions from SentinelCare

This is the `machine-detected event stream`.

### 4. Hospital digital source stream

Imported from:

1. HIS/EMR
2. lab
3. radiology
4. pharmacy
5. device systems
6. claims and audit systems

This is the `system-generated evidence stream`.

## Canonical ingestion pipeline

### Stage A. Source receipt

Receive:

1. form submissions
2. CSV uploads
3. API events
4. SentinelCare alert objects

### Stage B. Normalization

Convert all streams into a canonical event envelope:

1. source metadata
2. facility and department mapping
3. event timestamps
4. domain and process-stage mapping
5. identity/privacy handling

### Stage C. De-duplication and linkage

Identify:

1. same event reported manually and by SentinelCare
2. multiple reports from different departments about same case
3. repeated events belonging to one cluster

Link using:

1. encounter/time overlap
2. domain similarity
3. patient context similarity
4. trace IDs from SentinelCare

### Stage D. Classification

Assign:

1. domain
2. deviation class
3. severity
4. process stage
5. escalation path

### Stage E. Queue routing

Route based on:

1. facility-level ownership
2. district/state thresholds
3. sentinel-risk triggers
4. policy-defined escalation rules

### Stage F. Learning loop

Use review results to update:

1. surveillance thresholds
2. SentinelCare policies
3. agent decision rules
4. AI training labels

## Mapping between systems

### SentinelCare output -> India surveillance record

| SentinelCare field | India surveillance destination |
| --- | --- |
| alert_id | linked_system_trace_id |
| event_id | report_id or external_event_key |
| domain | domain |
| detection rationale | event_summary / trace evidence |
| severity | severity_level |
| route owner | review_owner_role |
| policy version | linked_policy_version |
| review actions | triage and closure history |

### Manual surveillance -> SentinelCare learning feedback

| India surveillance field | SentinelCare use |
| --- | --- |
| confirmed event type | supervised label |
| preventability | prioritization weight |
| closure quality | workflow quality metric |
| recurrence flag | model/policy tuning |
| contributing factors | causal feature enrichment |

## Role of the earlier agents in the integrated system

### Agent A: intake and source harmonization

1. accepts manual and machine streams
2. validates payload structure
3. adds source provenance

### Agent B: taxonomy mapper

1. maps event to domain and deviation
2. standardizes process-stage representation

### Agent C: deterministic detection engine

1. applies threshold rules
2. identifies required escalation

### Agent D: event linker and deduplicator

1. merges manual and machine detections
2. links related events into one case

### Agent E: queue and routing coordinator

1. assigns facility/state/national owner
2. creates due dates and urgency path

### Agent F: trace and narrative generator

1. creates explainable summaries
2. generates case trace for human review

### Agent G: governance and policy guard

1. checks active policies
2. enforces reporting and closure requirements

### Agent H: validation and learning monitor

1. compares machine detections with manual confirmations
2. produces calibration and surveillance quality feedback

## Recommended implementation path

### Phase 1

1. keep current daily manual form
2. add event-level case schema
3. create `source_mode`
4. allow SentinelCare-generated case insertion through API

### Phase 2

1. add de-duplication rules
2. add linked trace IDs
3. support machine-generated candidate cases requiring human confirmation

### Phase 3

1. unify dashboards
2. generate state/national signal clusters from both streams
3. use adjudicated data to tune AI and rule policies

## Conclusion

Yes, manual entry can and should be integrated with the earlier SentinelCare platform.

The right model is not to replace manual reporting with AI, but to combine:

1. human operational surveillance,
2. machine-generated detection,
3. shared governance,
4. shared auditability,
5. shared learning.
