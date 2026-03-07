# Multi-Agent Task Architecture (MVP)

This implementation follows the blueprint's Agent A-H model and maps each agent to a deterministic responsibility in the pipeline.

## Agent roles in code

- Agent A (`FounderProductArchitectAgent`): scope check for each incoming event.
- Agent B (`ClinicalKnowledgeEngineerAgent`): prepares rule context for encounter.
- Agent C (`DataInteroperabilityEngineerAgent`): normalization/audit marker for inbound event.
- Agent D (`DetectionMLEngineerAgent`): executes safety detections across three MVP engines.
- Agent E (`SafetyRedTeamEngineerAgent`): post-detection safety sanity check.
- Agent F (`ApplicationEngineerAgent`): routes alerts to role-specific recipients.
- Agent G (`DevSecOpsMLOpsEngineerAgent`): writes audit task metadata.
- Agent H (`ValidationDocumentationEngineerAgent`): records validation task metadata.

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

