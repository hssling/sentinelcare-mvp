# Figure and Table Package

## Figures

### Figure 1. Ten-domain SentinelCare patient safety taxonomy

Domains:

1. Medication safety
2. Diagnostic safety
3. Procedure and surgical safety
4. Deterioration surveillance
5. Infection prevention and environmental safety
6. Laboratory and radiology process safety
7. Care transition safety
8. Documentation and communication safety
9. Device and equipment safety
10. Operational safety

### Figure 2. Shared process-deviation grammar

Core deviation classes:

- omission
- contradiction
- harmful delay
- sequencing mismatch
- closure failure

### Figure 3. Common alert schema across domains

Required fields:

- why alert fired
- supporting evidence
- responsible owner
- deadline
- recommended action
- override policy

## Tables

### Table 1. Ten-domain taxonomy and exemplar hazards

| Domain | Exemplar hazard |
|---|---|
| Medication safety | contraindication, duplication, dose-adjustment error |
| Diagnostic safety | missed or delayed follow-up |
| Procedure and surgical safety | checklist deviation, wrong sequence |
| Deterioration surveillance | delayed escalation of worsening physiology |
| Infection/environmental safety | isolation or contamination control gap |
| Laboratory and radiology process safety | critical result not closed |
| Care transition safety | referral leakage, discharge follow-up gap |
| Documentation/communication safety | conflicting or missing plan documentation |
| Device/equipment safety | alarm, device setting, or maintenance failure |
| Operational safety | staffing, throughput, handoff, logistics risk |

### Table 2. Process-deviation classes and examples

| Deviation class | Example |
|---|---|
| Omission | missing renal dose adjustment |
| Contradiction | allergy-documented medication prescribed |
| Harmful delay | critical result not acknowledged on time |
| Sequencing mismatch | downstream action before prerequisite confirmation |
| Closure failure | finding acknowledged without documented resolution |

### Table 3. Common alert schema

| Field | Purpose |
|---|---|
| Reason | explain why the alert fired |
| Evidence | support traceability and trust |
| Owner | identify accountable role |
| Deadline | operationalize timeliness |
| Recommended action | guide next step |
| Override policy | control and document dissent |

### Table 4. Cross-domain process metrics

| Metric | Purpose |
|---|---|
| Time to detection | assess signal timeliness |
| Time to acknowledgement | assess ownership response |
| Time to action | assess workflow execution |
| Closure completion | assess end-to-end reliability |
| Override rate | assess burden and trust |
| No-action-after-alert rate | identify ineffective signal delivery |
| Harmful false-positive rate | assess safety cost |
