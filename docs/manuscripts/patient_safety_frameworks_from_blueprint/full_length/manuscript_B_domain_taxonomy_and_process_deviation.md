# A Unified Domain Taxonomy and Process-Deviation Framework for Multidomain Medical Error Intelligence

## Title page

### Full title

A Unified Domain Taxonomy and Process-Deviation Framework for Multidomain Medical Error Intelligence

### Short title

Taxonomy for multidomain safety intelligence

### Authors

[Author names and affiliations to be inserted]

### Corresponding author

[Name, institution, email to be inserted]

## Abstract

### Background

Healthcare harm emerges from heterogeneous pathways including medication management, diagnostic follow-up, procedures, transitions, documentation, devices, and operations. Existing safety programs often lack a shared taxonomy that is broad enough for system-level coverage yet structured enough for computation and operational action.

### Objective

To develop a multidomain patient safety taxonomy and process-deviation framework suitable for prospective risk detection, accountable routing, and comparable evaluation across clinical domains.

### Methods

We synthesized the domain structure and process logic defined in the SentinelCare founder blueprint and mapped them against literature on diagnostic safety, closed-loop communication, medication safety decision support, sepsis surveillance, and patient safety systems engineering. Domains were organized using a shared deviation grammar and common alert semantics.

### Results

The resulting framework defines ten safety domains and a unified process-deviation typology: omission, contradiction, harmful delay, sequencing mismatch, and closure failure. These deviations can be instantiated across domain-specific triggers while preserving a common alert schema that specifies evidence, owner, deadline, recommended action, and override policy.

### Conclusions

A unified domain-process framework enables scalable patient safety intelligence by separating universal workflow semantics from local clinical rules. This architecture supports staged deployment, cross-domain comparability, and operational accountability.

## Introduction

Patient safety science has long recognized that preventable harm is not confined to a single clinical setting or discipline. Medication errors, delayed diagnoses, critical result follow-up failures, surgical process breakdowns, deterioration escalation delays, and care transition gaps may appear operationally distinct, yet they share underlying features: broken sequences, weak communication, missed confirmation, and incomplete closure. The challenge for digital safety systems is to represent this complexity without collapsing into either excessive fragmentation or unusable abstraction.

Most current operational tools lean toward one of two extremes. Some are highly domain-specific, such as sepsis surveillance or medication interaction checking, and therefore offer local value but limited cross-domain integration. Others are broad safety reporting schemes that support governance and retrospective learning but provide weak real-time executability. A coherent patient safety intelligence platform needs both breadth and structure: breadth to capture diverse harms, and structure to support comparable computation, alerting, and workflow control.

The SentinelCare blueprint addresses this challenge by specifying ten safety domains and embedding them within a common process model. The underlying assumption is that patient safety can be standardized at the level of workflow deviation even when clinical content differs. A dose-adjustment omission, an unacknowledged critical result, and a delayed sepsis escalation are not clinically identical, but they can all be encoded as failures in expected process progression.

This manuscript presents a full-length framework for multidomain patient safety taxonomy and process deviation modeling derived from the SentinelCare blueprint and strengthened through current literature and guidance. The purpose is to define a theoretically durable, operationally actionable representation of safety events that can scale across domains without sacrificing local meaning.

## Methods

### Design source

The primary design source was the SentinelCare founder blueprint, which explicitly enumerated ten safety domains, user roles, event taxonomy, alert taxonomy, and a process representation based on Intent -> Action -> Confirmation -> Response -> Follow-up -> Closure. We treated the blueprint as a candidate conceptual model and assessed whether it could support a unified taxonomy suitable for computation and workflow execution.

### Review focus

Evidence and policy review focused on domain areas where cross-domain generalization is typically difficult:

1. medication safety and alerting,
2. diagnostic safety and test-result closure,
3. deterioration recognition,
4. workflow and communication reliability,
5. patient safety systems strategy.

Primary questions were:

1. Can distinct safety domains share common operational failure states?
2. What minimum common alert semantics are necessary for workflow accountability?
3. Which metrics can be standardized across heterogeneous safety domains?

### Framework synthesis

We first retained the ten-domain architecture from the blueprint. We then abstracted the process-deviation logic from the clinical process chain and tested whether each domain could be represented using the same limited set of deviation classes. The resulting taxonomy was iteratively refined to preserve both domain specificity and cross-domain comparability.

## Results

### Ten-domain patient safety taxonomy

The framework retains the ten domains defined in the blueprint:

1. medication safety,
2. diagnostic safety,
3. procedure and surgical safety,
4. deterioration surveillance,
5. infection prevention and environmental safety,
6. laboratory and radiology process safety,
7. care transition safety,
8. documentation and communication safety,
9. device and equipment safety,
10. operational safety.

This domain structure is broad enough to cover major contemporary safety burdens while remaining interpretable for health systems and governance bodies. It also aligns with the reality that the same patient encounter may traverse several domains within a short window.

### Shared deviation grammar

The key result of the synthesis is that these ten domains can be represented using a single deviation grammar:

1. omission,
2. contradiction,
3. harmful delay,
4. sequencing mismatch,
5. closure failure.

Omission captures missing expected steps, such as absent renal dose adjustment or missing discharge follow-up order. Contradiction captures discordance across sources, such as note findings that conflict with active orders or an allergy-documented medication being prescribed. Harmful delay captures timing breaches, including delayed acknowledgment of critical values or delayed deterioration escalation. Sequencing mismatch captures unsafe ordering of steps, such as incorrect procedural checklist progression or care transition processes executed without prerequisite confirmation. Closure failure captures unresolved pathways despite partial acknowledgment, such as a critical result acknowledged without documented action.

### Domain-specific instantiation

The shared deviation grammar becomes clinically meaningful through domain-specific triggers.

In medication safety, omission includes renal or hepatic dose-adjustment failures and omitted high-risk medications at discharge. Contradiction includes allergy conflicts, drug duplication, and interaction mismatches. Closure failure includes unresolved medication reconciliation discrepancies.

In diagnostic and critical-result follow-up, harmful delay is central. Critical test results may be reported but not acknowledged within policy windows. Closure failure occurs when acknowledged findings are not acted upon or tracked to resolution. Contradiction may arise between radiology findings and documented plans.

In deterioration surveillance, harmful delay and omission dominate. Rising-risk signals may not be escalated; sepsis bundle steps may not be completed; shock or hypoxia patterns may not trigger response in a timely fashion. Sequencing mismatch can occur when downstream steps occur before stabilization or before confirmation of bedside reassessment.

In care transitions, closure failure and omission become especially important. Referral leakage, discharge follow-up gaps, and medication reconciliation failures all represent discontinuities in the later parts of the process chain.

### Common alert semantics

A major consequence of the unified taxonomy is that all domains can use a common alert schema. Each actionable alert should minimally specify:

1. why the alert fired,
2. what evidence supports it,
3. who is responsible,
4. by when action is expected,
5. what action is recommended,
6. whether override is permitted and how it must be documented.

This common schema is not simply a convenience for software engineering. It is what permits operational accountability across otherwise diverse safety problems.

### Cross-domain metric standardization

The framework also supports shared metrics across domains:

1. time-to-detection,
2. time-to-acknowledgment,
3. time-to-action,
4. closure completion rate,
5. override rate,
6. no-action-after-alert rate,
7. harmful false-positive rate.

These metrics are more useful for platform evaluation than domain-specific counts alone because they reveal whether the system actually improves process reliability.

## Discussion

The proposed taxonomy matters because multidomain patient safety intelligence will fail without a durable representation language. If every domain uses its own local logic, event semantics, severity labels, and action structures, integration becomes fragile and governance becomes inconsistent. By contrast, if all domains are compressed into overly generic categories, the resulting system loses clinical meaning and usability.

The SentinelCare domain-process framework resolves this tension by standardizing the level of workflow deviation rather than the level of clinical content. This is a pragmatic and theoretically defensible compromise. It allows medication safety, test-result closure, and deterioration surveillance to share the same operational substrate while preserving domain-specific trigger logic. It also supports human-centered design, because alert explanation and action expectations can remain consistent across domains from the user’s perspective.

This approach further improves implementation tractability. It becomes feasible to build one event fabric, one alert schema, one queueing model, and one governance structure for multiple safety domains. That is a major advantage over point-solution proliferation. It also aligns with broader systems-safety thinking in which high-reliability operation depends on consistent detection and escalation patterns across diverse hazards.

The framework has limitations. It is a theoretical and architectural synthesis rather than a completed empirical cross-domain validation study. Some domains, particularly documentation contradictions, device safety, and operational logistics risk, may require more heterogeneous evidence sources and more sophisticated extraction logic than the MVP domains. Nonetheless, the common deviation grammar remains useful as a top-level organizing principle.

The most immediate application of this framework is to guide staged expansion beyond the first three pilot domains. Because the core semantics are shared, new domains can be introduced incrementally without rebuilding the operational substrate from scratch.

## Conclusion

A unified domain taxonomy and process-deviation framework provides the conceptual infrastructure required for scalable patient safety intelligence. The SentinelCare model enables cross-domain computation, accountable action, and comparable evaluation while preserving domain-specific clinical meaning. This framework supports the transition from isolated digital safety tools to integrated patient safety operations.

## Declarations

### Ethics approval and consent to participate

Not applicable.

### Consent for publication

Not applicable.

### Data availability

No patient-level dataset is reported in this manuscript.

### Code availability

Repository: https://github.com/hssling/sentinelcare-mvp

### Funding

[To be inserted]

### Author contributions

[To be inserted]

### Competing interests

[To be inserted]

## References

1. World Health Organization. Global Patient Safety Action Plan 2021-2030. Geneva: WHO; 2021. Available from: https://www.who.int/publications/i/item/9789240032705
2. World Health Organization. Global patient safety report 2024. Geneva: WHO; 2024. Available from: https://iris.who.int/handle/10665/376928
3. Institute for Healthcare Improvement. Safer Together: A National Action Plan to Advance Patient Safety. Boston: IHI. Available from: https://www.ihi.org/national-action-plan-advance-patient-safety
4. National Academies of Sciences, Engineering, and Medicine. Improving Diagnosis in Health Care. Washington, DC: The National Academies Press; 2015. Available from: https://www.nationalacademies.org/publications/21794
5. Callen J, Georgiou A, Li J, Westbrook JI. Closing the loop on test results to reduce communication failures: a rapid review of evidence, practice and patient perspectives. BMC Health Serv Res. 2020. Available from: https://pmc.ncbi.nlm.nih.gov/articles/PMC7510293/
6. Evans L, Rhodes A, Alhazzani W, et al. Surviving sepsis campaign: international guidelines for management of sepsis and septic shock 2021. Crit Care Med. 2021. Available from: https://pubmed.ncbi.nlm.nih.gov/34599691/
7. Joint Commission. National patient safety goals and critical test result communication FAQ. Available from: https://www.jointcommission.org/standards/standard-faqs/critical-access-hospital/national-patient-safety-goals-npsg/000001556
8. Slight SP, Beeler PE, Seger DL, et al. A cross-sectional observational study of high override rates of medication-related alerts in computerized provider order entry. BMJ Qual Saf. 2018. Available from: https://pubmed.ncbi.nlm.nih.gov/30463867/

