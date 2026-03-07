# SentinelCare App Overhaul Framework Mapping

## Purpose

This document translates the manuscript framework series into concrete application requirements so the product architecture follows the same theory, semantics, and governance model described in the publication package.

## Principle

The app should stop behaving like a demo dashboard with detached tables and instead behave like a patient safety operations system with explicit traces from:

`input data -> process interpretation -> detected deviation -> routed intervention -> closure -> governance review`

## Framework-to-product mapping

### Manuscript A -> system architecture and runtime traceability

Product requirements:

1. Show the `intent -> action -> confirmation -> response -> follow-up -> closure` chain for every processed event.
2. Expose the eight-layer architecture in the backend trace model:
   - data fabric
   - clinical knowledge
   - detection
   - prediction
   - intervention
   - learning
   - governance
   - experience
3. Persist per-event evidence, decision path, routed role, due time, closure state, and policy version.

UI requirements:

1. `Event Trace` page for one event or patient encounter.
2. `Safety Command Center` page for active queue and domain counts.
3. `Policy and Validation` page for active logic, version, and validation state.

### Manuscript B -> taxonomy and deviation-centered workflow

Product requirements:

1. Every alert must have:
   - domain
   - deviation class
   - severity
   - owner
   - due time
   - recommended action
   - override rule
2. The frontend must group alerts by:
   - domain taxonomy
   - deviation class
   - workflow state
3. Filters and analytics must be cross-domain, not only domain-specific.

UI requirements:

1. `Deviation Explorer` panel showing omission, contradiction, harmful delay, sequencing mismatch, and closure failure.
2. Domain-to-deviation matrix view.
3. Cross-domain metrics widgets:
   - time to detection
   - time to acknowledgement
   - time to action
   - closure completion
   - override rate

### Manuscript C -> governance and validation controls

Product requirements:

1. Every active rule or policy must expose:
   - policy state
   - approver
   - activation date
   - evidence basis
   - rollback state
2. Validation phase must be explicit:
   - retrospective
   - silent prospective
   - controlled pilot
   - scale-up
3. Every override and non-action event must be auditable.

UI requirements:

1. `Governance Console` with policy lifecycle states.
2. `Validation Workbench` with phase status and metrics.
3. `Alert Burden and Overrides` review panel.

## Required backend changes

### Event model

Extend event processing output to include:

1. `process_stage_trace`
2. `deviation_class`
3. `closure_requirements`
4. `active_policy_version`
5. `validation_phase`

### Alert model

Normalize alert schema to:

1. `alert_id`
2. `domain`
3. `deviation_class`
4. `severity`
5. `evidence_summary`
6. `owner_role`
7. `deadline_at`
8. `recommended_action`
9. `override_policy`
10. `closure_state`

### Governance model

Persist:

1. policy lifecycle states
2. approval history
3. override logs
4. release-gate decisions
5. validation-report history

## Required frontend overhaul

### Phase 1

1. Replace current landing page with a real operations shell:
   - live queue
   - recent events
   - domain/deviation counts
   - validation banner
2. Add patient/event trace drawer.
3. Add explanation cards for what the system saw, why the alert fired, and what counts as closure.

### Phase 2

1. Add governance console.
2. Add validation metrics dashboard.
3. Add role-based worklists and action forms.

### Phase 3

1. Add ingest adapters for real clinical feeds.
2. Add silent-mode deployment controls.
3. Add retrospective review and adjudication workflows.

## Immediate implementation sequence

1. Refactor backend contracts so deviation class and process trace are first-class fields.
2. Expose a new explainability endpoint:
   - `GET /trace/{event_id}`
3. Redesign frontend around four primary views:
   - command center
   - event trace
   - governance console
   - validation workbench
4. Populate the UI with both simulated and persisted traces so the product demonstrates the full theory, not just alert rows.
