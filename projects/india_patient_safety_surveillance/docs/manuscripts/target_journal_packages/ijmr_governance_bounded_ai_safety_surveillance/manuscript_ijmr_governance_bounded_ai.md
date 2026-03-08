# Governance, accountability, and bounded AI in patient safety surveillance: an implementation framework for India

## Abstract

Patient safety surveillance systems can fail for governance reasons as often as for technical ones. Reporting infrastructures that lack accountability, auditability, review ownership, and bounded decision support frequently produce administrative burden without reliable prevention. This paper synthesizes guidance and literature on patient safety governance, clinical decision-support oversight, learning-system accountability, and AI governance to propose an implementation framework for India. We argue that patient safety surveillance should be governed as a layered public health and health-systems function, with explicit roles at facility, state, and national levels; auditable case ownership; documented closure and corrective action pathways; and clear restrictions on what AI may and may not do. AI can usefully assist with narrative structuring, classification support, clustering, and summarization, but should not replace human judgment in severity attribution, punitive action, or serious-case closure. A governance-first design is necessary if digital patient safety surveillance in India is to support learning, trust, and prevention at scale.

**Keywords:** patient safety, governance, accountability, artificial intelligence, surveillance, India

## Introduction

Patient safety reporting systems are often discussed as technical infrastructures, but their success depends fundamentally on governance. Data capture without ownership, escalation discipline, closure standards, and policy feedback creates institutional archives rather than prevention systems. This is especially important in surveillance systems, where reports move across multiple organizational levels and where learning depends on trust as much as on technology.<sup>1-3</sup>

Digital expansion intensifies this governance problem. As more reporting, triage, and analytical functions become digitized, health systems face new questions about transparency, reviewability, and the role of algorithmic assistance. The WHO, regulatory agencies, and broader health AI governance literature increasingly emphasize accountability, human oversight, and fitness for purpose as core conditions for safe deployment.<sup>4-7</sup>

India’s emerging patient safety and digital health environment creates an opportunity to build governance into surveillance architecture from the start. Rather than retrofitting accountability after large-scale deployment, the governance model should define who may report, review, escalate, classify, close, and learn from safety events, and where AI support must remain bounded by human responsibility.

## Methods

This paper was developed as a structured narrative review and framework synthesis. Literature and guidance on patient safety governance, reporting-and-learning systems, digital health accountability, audit design, and AI governance were reviewed from WHO sources, regulatory guidance, peer-reviewed literature, and Indian digital health context documents. The goal was to derive implementation requirements for a governed patient safety surveillance architecture suitable for India.

## Governance requirements for safety surveillance

At minimum, patient safety surveillance requires five governance functions.

### Ownership

Each report or event case should have a clearly assigned reviewer or review team. Unowned reports become administratively stagnant and erode trust.

### Escalation logic

Serious or recurrent events require escalation rules that are visible, documented, and auditable. Escalation should not depend entirely on individual initiative.

### Closure quality

Case closure should represent reviewed learning and documented action, not merely status disposal. Closure quality should be auditable.<sup>1,2</sup>

### Policy linkage

Surveillance should feed policy revision, training, and corrective action rather than remain confined to a dashboard environment.

### Auditability

Systems should preserve who saw what, who classified what, who changed what, and on what basis. This is necessary for accountability and credibility.

## Why bounded AI matters

AI can be helpful in patient safety surveillance, but its acceptable role is narrower than many product narratives imply. In surveillance workflows, AI is most defensible when used to reduce clerical burden and improve information structuring. It is least defensible when used to replace human accountability in serious-case decision making.<sup>4-7</sup>

Acceptable bounded uses include:

- narrative-to-structured-field extraction
- taxonomy and severity suggestion
- clustering of similar cases
- summarization for review meetings
- draft CAPA prompts for human review

Unacceptable or high-risk uses include:

- autonomous final severity assignment for serious cases
- punitive attribution
- unsupervised case closure
- suppression of reports without human review
- opaque recommendation systems that cannot be audited

## An implementation framework for India

For India, a governance-first safety surveillance architecture should define distinct responsibilities at facility, state, and national levels.

- Facilities should own intake, immediate containment, basic review, and local corrective action.
- State structures should own aggregation, escalation review, benchmarking interpretation, and coordinated learning.
- National structures should own taxonomy, standards, policy synthesis, and meta-governance.

AI services should sit inside this hierarchy as assistive components, not governing actors. Their outputs should be logged, attributable, reviewable, and overrideable.

## Discussion

The core design challenge is not whether AI can be added to safety surveillance. It is whether safety surveillance can remain accountable after AI is added. The literature suggests that trust, oversight, and explicit workflow ownership are decisive. In India, these considerations are even more important because surveillance will have to operate across heterogeneous institutions and digital maturity levels. A governance-light AI-enhanced system would be operationally brittle and ethically exposed.

## Conclusion

Patient safety surveillance should be governed as a layered accountability system before it is treated as an analytics platform. AI can improve throughput and structuring, but only within bounded, transparent, and reviewable roles. For India, governance-first design is the safest path to national-scale digital patient safety learning.

## References

1. World Health Organization. Global patient safety action plan 2021-2030. Geneva: WHO; 2021.
2. World Health Organization. Global patient safety report 2024. Geneva: WHO; 2024.
3. Benn J, Koutantji M, Wallace L, Spurgeon P, Rejman M, Healey A, et al. Feedback from incident reporting: information and action to improve patient safety. Qual Saf Health Care. 2009;18:11-21.
4. US Food and Drug Administration. Clinical decision support software guidance. Silver Spring: FDA; 2022.
5. US Food and Drug Administration, Health Canada, Medicines and Healthcare products Regulatory Agency. Good machine learning practice for medical device development: guiding principles. 2021.
6. World Health Organization. Ethics and governance of artificial intelligence for health. Geneva: WHO; 2021.
7. HealthIT.gov. Decision support interventions. Office of the National Coordinator for Health Information Technology.
