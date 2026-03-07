# Figure and Table Package

## Figures

### Figure 1. SentinelCare process-control model for patient safety

Conceptual figure showing the core safety chain:

`Intent -> Action -> Confirmation -> Response -> Follow-up -> Closure`

Each stage is associated with computable failure modes:

- missing action
- delayed action
- contradictory evidence
- absent owner
- acknowledgement without closure

**Legend:** The figure illustrates the common process grammar used across safety domains. SentinelCare treats a safety event as a deviation within this chain rather than as a disconnected alert or retrospective report category.

### Figure 2. SentinelCare eight-layer architecture

Stacked architecture figure showing:

1. Data fabric
2. Clinical knowledge
3. Detection
4. Prediction
5. Intervention
6. Learning
7. Governance
8. Experience

**Legend:** The architecture links data ingestion and safety logic to workflow, learning, and governance. It is designed to ensure that patient safety signals are actionable, auditable, and adaptable within local clinical environments.

### Figure 3. Translational evaluation pathway

Three-stage pathway:

1. Retrospective rule and cohort validation
2. Silent prospective deployment
3. Controlled interruptive intervention

Output measures:

- positive predictive value
- time to detection
- time to acknowledgement
- time to corrective action
- override rate
- queue overdue rate
- harm-related process outcomes

**Legend:** The figure shows the recommended evaluation strategy for SentinelCare pilots. The staged pathway is intended to reduce implementation risk and avoid premature live deployment of interruptive patient safety logic.

## Tables

### Table 1. SentinelCare architectural layers and safety functions

| Layer | Primary function | Example outputs |
|---|---|---|
| Data fabric | Normalize and reconcile heterogeneous source data | Time-aligned patient-event stream |
| Clinical knowledge | Encode policies, protocols, and local rules | Computable safety rules and escalation policies |
| Detection | Identify rule violations, contradictions, and process deviations | Trigger candidates, watchlist states |
| Prediction | Estimate near-term risk trajectories | Risk scores, deterioration forecasts |
| Intervention | Route, prioritize, and operationalize action | Alerts, tasks, escalation workflows |
| Learning | Capture feedback and recalibrate logic | Override review, drift analysis |
| Governance | Maintain version control, approval, and audit | Active policies, validation reports, rollback artifacts |
| Experience | Present role-specific views and controls | Clinician worklists, safety command dashboards |

### Table 2. SentinelCare near-term pilot domains

| Domain | Core problem | Example computable triggers | Primary operational outcome |
|---|---|---|---|
| Medication safety | Contraindication, duplication, inappropriate dosing, allergy mismatch | Duplicate therapy, renal dosing gap, allergy conflict | Time to order correction or pharmacist review |
| Critical-result follow-up | Delay or failure in acknowledgment and action | Unacknowledged critical lab or imaging result beyond threshold | Time to acknowledgment and action closure |
| Deterioration surveillance | Delayed recognition or escalation in worsening patients | Abnormal trends, sepsis bundle delay, shock-risk escalation | Time to escalation and treatment initiation |

### Table 3. Guideline and evidence alignment

| External source | Design implication | SentinelCare response |
|---|---|---|
| WHO patient safety strategy | Treat safety as a system property requiring learning and accountability | Multilayer architecture with governance and learning loops |
| National Academies diagnostic safety report | Close the loop on diagnostic processes | Critical-result follow-up and closure tracking |
| Medication CDS literature | Optimize relevance and minimize alert fatigue | Evidence payloads, role routing, override review |
| Surviving Sepsis Campaign | Prioritize timely identification and escalation | Deterioration watchlists and escalation workflows |
| FDA CDS and GMLP guidance | Preserve transparency, intended use clarity, and lifecycle controls | Human-governed design, policy versioning, auditability |
| ONC DSI criteria | Expose source attributes and feedback pathways | Provenance-aware alerts and structured review capture |

### Table 4. Proposed validation pathway and core metrics

| Phase | Purpose | Core metrics |
|---|---|---|
| Retrospective validation | Establish rule fidelity and cohort definitions | PPV, event capture rate, chart-review agreement |
| Silent prospective mode | Assess operational burden without interruptive action | Alert burden, acknowledgement lag, no-action rate |
| Controlled intervention | Measure workflow effect and safety process benefit | Time to action, escalation completion, harmful false positives |

## Assembly guidance

1. Submit the main manuscript with embedded table callouts.
2. Upload tables as editable files if requested by the submission system.
3. Export each figure as a publication-quality vector or high-resolution raster graphic before formal submission.
4. Keep total count within JAMIA Open `Research and Applications` limits: up to 4 tables and 6 figures.
