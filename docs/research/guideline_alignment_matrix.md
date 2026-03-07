# Guideline Alignment Matrix

## Scope

Maps SentinelCare MVP capabilities to guideline and evidence expectations.

## Matrix

| Domain | External expectation | Source | SentinelCare implementation status | Gap |
|---|---|---|---|---|
| Medication safety | CPOE/CDS reduces harm when implemented with usable alert design | https://pubmed.ncbi.nlm.nih.gov/30463867/ | Rule-based contraindication, dose adjustment, duplicate checks | Needs live formulary + patient-specific medication history ingestion |
| Critical result closure | Timely communication, acknowledgment, and action responsibility | https://www.jointcommission.org/standards/standard-faqs/critical-access-hospital/national-patient-safety-goals-npsg/000001556 | Unacknowledged critical result alerts and queue escalation | Needs real role-directory integration and SLA audit exports |
| Deterioration/sepsis | Early identification with protocolized escalation | https://pubmed.ncbi.nlm.nih.gov/34599691/ | Risk watchlist, sepsis bundle deviation, delayed escalation alerts | Needs validated temporal models and prospective silent-mode trial |
| Diagnostic safety | Closed-loop follow-up to reduce missed/delayed diagnoses | https://www.nationalacademies.org/publications/21794 | Basic follow-up and no-action reminders | Needs longitudinal referral and outpatient closure tracking |
| AI/ML governance | Lifecycle quality controls, documentation, and transparency | https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles | Policy submission/approval APIs and validation reporting | Needs model cards, change control board workflow, drift monitoring |
| Explainability in CDS | Source attribution and intervention transparency | https://www.healthit.gov/test-method/decision-support-interventions | Alert evidence payload + recommended action fields | Needs UI-level source citation and provenance links |
| Safety program maturity | System-level safety governance and learning loops | https://www.ihi.org/national-action-plan-advance-patient-safety | Queue, review actions, validation reports | Needs incident review governance cadence and board reporting package |

## Interpretation

1. MVP aligns with guideline direction at architecture level.
2. Major remaining gaps are operational integration, validation rigor, and production governance.
3. Manuscripts should position current stage as translational prototype with staged clinical validation plan.

