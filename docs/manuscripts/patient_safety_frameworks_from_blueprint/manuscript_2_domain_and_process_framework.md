# Manuscript 2: Domain Taxonomy and Process-Deviation Framework for Medical Error Intelligence

## Proposed Title

A Unified Domain and Process-Deviation Framework for Multidomain Medical Error Detection and Prevention

## Abstract

### Background

Clinical harm emerges through heterogeneous patterns spanning medication, diagnostics, procedures, deterioration, transitions, and operations. Fragmented safety taxonomies limit scalable computable surveillance.

### Objective

To define a unified multidomain taxonomy and process-deviation framework that supports prospective error detection across complex healthcare workflows.

### Framework

The framework operationalizes ten safety domains and maps each domain to process-chain failure modes: omission, contradiction, delay, sequencing error, and closure failure. It pairs domain-specific trigger classes with standardized alert semantics, ownership metadata, and escalation obligations.

### Contribution

The framework enables consistent representation of diverse safety risks while preserving domain-specific clinical logic. It supports staged implementation, cross-domain learning, and comparable evaluation across pilot and scale-up deployments.

## 1. Introduction

Patient safety programs often suffer from two opposing problems:

1. narrow tools with high local precision but no portability,
2. broad taxonomies with limited operational executability.

The SentinelCare blueprint proposes a middle path: a unified framework with standardized process semantics and domain-specific trigger logic.

## 2. Domain Taxonomy

The framework defines ten domain classes:

1. medication safety,
2. diagnostic safety,
3. procedure/surgical safety,
4. deterioration surveillance,
5. infection prevention/environmental safety,
6. laboratory/radiology process safety,
7. care transition safety,
8. documentation/communication safety,
9. device/equipment safety,
10. operational safety.

## 3. Process-Deviation Typology

Every domain event is evaluated through a shared deviation grammar:

1. omission (expected action not executed),
2. contradiction (discordant evidence across sources),
3. harmful delay (time threshold breached),
4. sequencing mismatch (order of actions unsafe),
5. closure failure (issue unresolved despite acknowledgement).

This grammar enables comparable logic across otherwise dissimilar clinical contexts.

## 4. Event and Alert Standardization

The framework uses event-normalized inputs and shared alert schema:

Alert minimum fields:

1. why it fired,
2. evidence source,
3. actor responsible,
4. action deadline,
5. recommended next step,
6. override policy.

This standardization improves both workflow usability and governance traceability.

## 5. Domain-specific Examples

### Medication domain

Mapped deviations:

1. contraindication contradictions,
2. renal/hepatic adjustment omissions,
3. duplicate therapy sequencing errors,
4. discharge reconciliation closure failures.

### Critical-result closure domain

Mapped deviations:

1. unacknowledged critical values (delay),
2. acknowledged-without-action (closure failure),
3. pending critical result post-discharge (transition omission).

### Deterioration domain

Mapped deviations:

1. rising-risk watchlist thresholds,
2. sepsis-bundle process deviations,
3. delayed escalation timing failures.

## 6. Framework for Accountability

To move from detection to prevention, each alert must bind:

1. a designated owner role,
2. escalation chain,
3. review and override logging,
4. closure status.

This converts passive alerts into enforceable workflow units.

## 7. Evaluation Structure

Cross-domain comparability is enabled by common metrics:

1. detection timeliness,
2. owner acknowledgment timeliness,
3. closure completeness,
4. harmful false-positive rate,
5. no-action-after-alert rate.

Domain-specific extensions can be layered without breaking core comparability.

## 8. Discussion

A unified domain-process framework improves scalability by separating:

1. universal process semantics,
2. local clinical logic.

This structure supports both site adaptation and governance consistency.

## 9. Conclusion

The proposed taxonomy and deviation framework offers a robust theoretical base for multidomain safety intelligence. It is suitable for staged implementation beginning with narrow, high-value domains and expanding under common operational semantics.

