# Theoretical Framework for SentinelCare

## 1. Conceptual basis

SentinelCare is modeled as a socio-technical safety control system:

1. Signal capture from care processes
2. Risk inference under uncertainty
3. Action recommendation with accountable ownership
4. Escalation and closure tracking
5. Learning and governance feedback loops

This avoids framing the platform as autonomous diagnosis/treatment and instead positions it as a high-reliability safety layer.

## 2. Process model

Core chain:

`Intent -> Action -> Confirmation -> Response -> Follow-up -> Closure`

Error states are formalized as:

1. Omission of expected step
2. Unsafe contradiction
3. Delay beyond acceptable window
4. Ownership ambiguity
5. Unclosed critical loop

## 3. Agentic implementation model

Agents A-H are orchestrated software roles, not independent clinician-replacing models.

1. A-C: scope, policy context, normalization
2. D-E: detection + safety challenge
3. F: routing/escalation
4. G-H: audit, governance, validation

Each agent contributes traceable tasks to an auditable chain.

## 4. Causal assumptions

Primary causal hypothesis:

`Earlier, higher-precision detection + accountable routing + closed-loop follow-up -> lower preventable harm`

Mediators:

1. Time-to-detection
2. Time-to-acknowledgment
3. Time-to-action
4. Closure completeness

Moderators:

1. Workflow fit
2. Staffing load
3. Data quality
4. Site-specific policy calibration

## 5. Evaluation logic

Stage-wise evaluation:

1. Offline retrospective: event-level discrimination and calibration
2. Silent prospective: burden/timeliness without intervention risk
3. Controlled live pilot: safety outcomes with governance oversight
4. Scale-up: multi-site transportability and drift monitoring

