# Multi-Agent Task Architecture (MVP)

This implementation follows the blueprint's Agent A-H model and maps each agent to a deterministic responsibility in the pipeline.

## Agent roles in code

- Agent A (`FounderProductArchitectAgent`): `scope-check`, `pilot-domain-priority`.
- Agent B (`ClinicalKnowledgeEngineerAgent`): `rule-context-build`, `policy-version-selection`.
- Agent C (`DataInteroperabilityEngineerAgent`): `event-normalization`, `terminology-mapping`.
- Agent D (`DetectionMLEngineerAgent`): `detection-run`, `risk-score-aggregation`.
- Agent E (`SafetyRedTeamEngineerAgent`): `adversarial-sanity-check`, `false-positive-risk-triage`.
- Agent F (`ApplicationEngineerAgent`): `route-and-notify`, `escalation-path-evaluation`.
- Agent G (`DevSecOpsMLOpsEngineerAgent`): `audit-log-write`, `release-gate-check`.
- Agent H (`ValidationDocumentationEngineerAgent`): `validation-record`, `quality-report-update`.

## End-to-end lifecycle

1. Ingest event.
2. Run Agent A/B/C tasks.
3. Execute domain engines:
   - medication safety
   - critical-result closure
   - deterioration surveillance
4. Run Agent D/E tasks.
5. Route alerts via Agent F.
6. Record audit/validation tasks via Agent G/H.
7. Capture human review action to close alert.

## Why this architecture

The system is intentionally modular:

- easy to split each agent into a microservice later
- deterministic and testable baseline for governance
- direct alignment with the founder blueprint's pilot domains
