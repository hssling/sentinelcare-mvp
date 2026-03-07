# Building a federated patient safety surveillance system for India: a digital public health framework for reporting, learning, governance, and prevention

## Abstract

Patient safety remains an under-institutionalized health-systems function in many low- and middle-income settings, where avoidable harm is often recognized episodically, documented inconsistently, and learned from incompletely. In India, safety-related information is distributed across quality programmes, facility registers, morbidity and mortality review processes, pharmacovigilance structures, accreditation requirements, and increasingly fragmented digital platforms. Yet there is no widely implemented, federated architecture that links facility-level reporting, event-level investigation, subnational aggregation, governance review, and learning-oriented prevention in a single operational model. We conducted a structured narrative review of patient safety reporting and learning systems, digital health architecture, governance frameworks, and Indian policy and standards documents to derive design requirements for a national patient safety surveillance system. The proposed framework separates daily operational surveillance from event-level case learning, embeds facility, state, and national functions, supports interoperable digital ingestion and manual reporting, and places AI within a bounded assistive role rather than an autonomous decision-making role. A federated Indian patient safety surveillance system should be designed as a learning infrastructure with clear taxonomy, denominators, review workflows, governance controls, and integration readiness, rather than as a passive incident repository.

**Keywords:** patient safety, surveillance, India, digital health, incident reporting, learning health system, governance

## Introduction

Unsafe care is now recognized as a major and preventable contributor to morbidity, mortality, inefficiency, and erosion of trust across health systems. The global policy movement on patient safety has increasingly shifted from isolated quality-improvement projects toward system-wide reporting, learning, and governance. The WHO Global Patient Safety Action Plan 2021-2030 and the WHO Global Patient Safety Report 2024 emphasize that health systems need stronger reporting and learning structures, safer processes, better workforce capability, and mechanisms for transforming incident information into preventive action rather than merely documenting failure.¹˒²

In India, the need for such a shift is especially important. The health system is large, mixed, heterogeneous, and operationally decentralized. Safety-relevant information exists across hospitals, medical colleges, laboratories, accreditation activities, disease surveillance systems, pharmacovigilance structures, and programme-specific reporting mechanisms. However, these streams do not yet function as an integrated patient safety surveillance and learning system. In many facilities, incident review remains episodic, heavily narrative, difficult to aggregate, and weakly connected to preventive governance. In other settings, adverse events may be known locally but not converted into structured, comparable, and escalatable intelligence.

At the same time, India is expanding digital public health and digital health infrastructure. The Ayushman Bharat Digital Mission (ABDM) is building foundational digital health architecture for identity, registries, and interoperability.³˒⁴ The Integrated Health Information Platform (IHIP) has demonstrated the operational importance of digital surveillance concepts for large-scale public health monitoring.⁵ These developments create an opportunity to think beyond facility-bound incident registers and toward a federated patient safety surveillance model that is digitally ready, operationally layered, and governance-oriented.

The challenge is not only technical. Incident reporting systems fail when they are punitive, poorly classified, disconnected from feedback, weakly governed, or incapable of supporting learning. Reviews of patient safety learning systems have repeatedly shown barriers such as fear of blame, limited feedback, unclear reporting rules, poor organizational support, and inadequate learning loops.⁶˒⁷ Therefore, a useful Indian framework must integrate taxonomy, workflows, governance, denominators, and learning functions rather than merely digitizing reporting forms.

This paper synthesizes the relevant literature and policy context and proposes a framework for a federated patient safety surveillance system for India. The goal is not to claim implementation effectiveness, which still requires prospective study, but to define a defensible systems architecture that can support reporting, learning, governance, and prevention at scale.

## Methods

This manuscript was developed as a structured narrative review and framework synthesis. The objective was to identify the conceptual, operational, and architectural requirements for a patient safety surveillance system suitable for India.

### Search approach

Literature and policy sources were identified through purposive searches of PubMed, PubMed Central, WHO publications, Indian government and public institutional websites, and key standards and governance sources relevant to patient safety, digital health, reporting systems, and surveillance. Search themes included combinations of the following concepts: patient safety, incident reporting, reporting and learning systems, surveillance, digital health, interoperability, governance, public health informatics, India, ABDM, IHIP, accreditation, and ethical or regulatory frameworks.

### Source domains

Sources were selected from five domains:

1. global patient safety frameworks and governance documents;
2. literature on incident reporting and patient safety learning systems;
3. Indian digital health and surveillance architecture sources;
4. Indian quality, accreditation, and ethics sources;
5. literature and guidance relevant to AI-supported but human-governed clinical or safety workflows.

### Inclusion logic

We prioritized documents and studies that were directly informative for national or subnational patient safety system design. These included WHO policy documents, Indian official digital health or health system sources, accreditation or governance standards, and peer-reviewed literature describing patient safety reporting systems, learning systems, and implementation barriers or enablers. Articles that focused solely on narrow specialty workflows without broader implications for surveillance architecture were not emphasized.

### Synthesis strategy

The final framework was built by extracting recurrent system requirements from the literature and policy documents and organizing them into six design layers:

1. reporting and intake;
2. event and denominator data model;
3. review and learning workflows;
4. digital interoperability;
5. governance and audit;
6. bounded AI assistance.

This synthesis was interpretive and framework-oriented rather than quantitative. No human participants were enrolled, and no primary patient data were analyzed.

## Why India needs a federated patient safety surveillance model

Patient safety surveillance in India cannot be reduced to a single national portal. The operational environment is too diverse for a purely centralized model, while a fully local model fails to support comparability and learning. What is required is a federated structure in which facilities retain operational responsibility for reporting and initial review, while state and national levels perform aggregation, benchmarking, signal management, governance oversight, and policy response.

Several structural realities support this conclusion.

First, avoidable harm presents through multiple mechanisms. Some signals are visible only at point of care, such as medication contradictions or delayed escalation in deterioration. Others become visible only through aggregation across departments or facilities, such as recurrent diagnostic delays, communication failures, or persistent equipment-related harm. A national system must therefore accommodate both local immediacy and higher-level pattern detection.

Second, patient safety requires denominators. A count of adverse events is not enough without context such as patient-days, admissions, surgeries, deliveries, or critical result volumes. Daily operational surveillance and event-level case review are related but different functions. A mature system needs both.

Third, governance is indispensable. Incident reporting without feedback and action creates fatigue, concealment, or symbolic compliance. A surveillance system should support escalation, auditability, corrective and preventive action tracking, and policy loops. This is consistent with the broader patient safety literature, which emphasizes that learning systems depend not merely on reporting frequency but on non-punitive culture, structured analysis, and visible learning cycles.⁶˒⁷

Fourth, India’s evolving digital health landscape makes interoperability both possible and necessary. ABDM offers building blocks for registries and interoperable exchange; IHIP demonstrates the value of digital surveillance architecture for large systems; and NABH-linked quality processes create a natural interface for facility governance and comparability.³⁻⁵˒⁸ A patient safety surveillance system that is not designed for interoperability risks becoming another silo.

## A proposed architectural model

### 1. Two linked reporting streams

The framework should explicitly separate:

- `daily operational surveillance`
- `event-level learning cases`

Daily operational surveillance captures denominators and burden indicators at department level, including patient-days, admissions, critical result counts, near misses, harm events, severe events, and relevant contextual stressors such as staffing shortfall, crowding, or system downtime. These data are useful for routine monitoring, basic alerts, and facility or district review.

Event-level learning cases capture richer incident information when a report warrants investigation or structured learning. These records should include encounter setting, process stage, deviation class, actual and potential harm, preventability, detectability, contributing factors, immediate actions, CAPA, ownership, and closure quality. This separation prevents the common failure of overloading daily forms with investigative detail while still preserving an escalation path into deeper review.

### 2. A canonical safety taxonomy

For comparability, the system requires a standard taxonomy that maps incidents into common classes. At minimum, the taxonomy should include:

- safety domain
- deviation class
- process stage
- severity level
- actual harm
- potential harm
- contributing factors
- preventability rating
- closure status

Without this canonical structure, multi-facility aggregation becomes a narrative archive rather than a learning system.

### 3. Layered review functions

The system should distribute work across levels:

- department and facility teams for submission, initial triage, and immediate containment;
- district or state review teams for aggregation, trend interpretation, and escalation;
- national teams for governance, benchmarking, synthesis, and policy feedback.

This structure matches how surveillance becomes useful: local teams act fastest, but higher levels detect cross-site patterns and system-level failures.

### 4. Signal detection and escalation

The architecture should support both rule-based and pattern-based signals. Rule-based alerts may be triggered by thresholds such as clusters of severe events, repeated closure failures, or recurrent incidents within a defined period. Pattern-based signals may emerge from repeated event-case similarity, domain spikes, or atypical combinations of burden and severity.

Every signal should preserve traceability:

- what triggered it
- which units it affected
- who owns next action
- whether corrective action was completed

### 5. Governance and audit

The surveillance system should include durable audit trails, policy linkage, role-aware permissions, and documented closure logic. Governance is not an add-on; it is what distinguishes learning from passive reporting. Policy versions, escalations, and CAPA records should be queryable and reviewable.

## Digital integration requirements

India’s future patient safety surveillance system should be interoperable rather than monolithic.

### ABDM-aligned readiness

ABDM provides a relevant enabling direction through digital identity, registries, and interoperability-oriented infrastructure.³˒⁴ A patient safety surveillance platform should be able to use these assets without being dependent on them for all workflows. Facility, department, and provider identities should be mappable to standardized registries where available.

### Manual-plus-digital ingestion

The system should accept more than one input mode:

1. manual department submissions
2. manually entered event cases
3. imported digital events from hospital systems
4. machine-detected cases or signals from prospective safety tools such as SentinelCare

This is important because many Indian facilities will initially operate in mixed digital maturity states. A surveillance system that only works with fully digital institutions will exclude much of the real care ecosystem; one that only supports manual entry will not scale well for digital hospitals.

### Data protection and minimality

Not every signal requires identifiable patient detail at higher levels. Facility-level investigation may require identifiable information, but state and national learning layers should preferentially use minimized, structured, role-appropriate records. This protects confidentiality while preserving learning utility.

## Where AI can and cannot help

There is growing interest in applying AI to safety reporting and classification. However, a national patient safety surveillance system should use AI cautiously and transparently.

### Appropriate uses

AI can be helpful in bounded tasks such as:

- converting free-text narratives into structured candidate fields;
- suggesting domain and deviation classes;
- clustering similar incidents across facilities;
- drafting concise summaries for reviewers;
- surfacing missing information for investigation;
- supporting trend interpretation and bulletin drafting.

These uses reduce review burden and improve consistency without displacing human authority.

### Inappropriate uses

AI should not autonomously:

- determine final severity in serious cases;
- assign blame or punitive consequence;
- close serious cases;
- replace governance review;
- make unsupported claims about causality.

The WHO and broader health AI governance literature emphasize the need for transparency, accountability, human oversight, and fitness for purpose.²˒⁹ In the Indian context, these principles are especially important because patient safety systems must build trust, not deepen opacity.

### Governance requirements for AI

An AI-enabled patient safety system should document:

- provider and model used;
- task purpose;
- human reviewer override;
- confidence or uncertainty marker where appropriate;
- audit trail of AI-assisted outputs.

In other words, AI should function as an assistive layer within governance, not as the governance mechanism itself.

## Implementation priorities for India

A realistic national rollout should proceed in stages.

### Stage 1: facility and state pilot

Initial pilots should focus on:

- a minimum daily surveillance dataset;
- event-case escalation workflow;
- a standard taxonomy;
- state surveillance cell review;
- dashboard and audit functions.

### Stage 2: interoperability and benchmarking

Once operational use stabilizes, the next step should be:

- mapping to digital facility and provider registries;
- ingestion from hospital information systems where feasible;
- cross-facility comparisons using stable denominators;
- district and state-level signal definitions.

### Stage 3: advanced learning and prevention

Only after stable data quality and review maturity should the system expand into:

- AI-assisted triage at scale;
- prospective signal ingestion from digital safety tools;
- benchmark reporting;
- policy dashboards;
- research and publication outputs on burden, trends, and intervention effects.

## Strengths and limitations of the proposed framework

The main strength of this framework is that it integrates patient safety reporting, surveillance, learning, and governance rather than addressing them as separate programmes. It is also designed explicitly for Indian health-system realities, including mixed digital maturity and layered governance.

The main limitation is that this paper is conceptual and review-based. It does not provide prospective implementation outcomes, burden estimates from multicentric deployment, or measured effect on harm reduction. Those will require phased piloting and evaluation using robust designs. The framework should therefore be interpreted as a systems blueprint for implementation and study, not as proof of effectiveness.

## Conclusion

India needs a patient safety surveillance system that does more than collect incident narratives. A scalable system must distinguish routine surveillance from event-level learning, use a common taxonomy, support facility-to-national review functions, preserve auditability, and be interoperable with the country’s evolving digital health architecture. AI may help with classification and summarization, but the system must remain human-governed and prevention-oriented. A federated patient safety surveillance model offers a realistic path for converting fragmented safety information into structured learning and safer health-system action in India.

## References

1. World Health Organization. Global patient safety action plan 2021-2030: towards eliminating avoidable harm in health care. Geneva: WHO; 2021.
2. World Health Organization. Global patient safety report 2024. Geneva: WHO; 2024. Available from: https://iris.who.int/handle/10665/376928, accessed on March 8, 2026.
3. National Health Authority. Ayushman Bharat Digital Mission resources. Available from: https://www.abdm.gov.in/resources, accessed on March 8, 2026.
4. National Health Authority. About Ayushman Bharat Digital Mission. Available from: https://nha.gov.in/NDHM, accessed on March 8, 2026.
5. Ministry of Health and Family Welfare, Government of India. Integrated Health Information Platform. Available from: https://ihip.mohfw.gov.in/, accessed on March 8, 2026.
6. Health Quality Ontario. Patient safety learning systems: a systematic review and qualitative synthesis. Ont Health Technol Assess Ser 2017;17:1-23. Available from: https://pmc.ncbi.nlm.nih.gov/articles/PMC5357133/, accessed on March 8, 2026.
7. Kuitunen I, Ponkilainen V, Hallila H, Nuutinen M, Alanen V, Reponiemi T, et al. Patient safety incident reporting and learning guidelines implemented by health care professionals in specialized care units: scoping review. J Med Internet Res 2024;26:e55971. Available from: https://pmc.ncbi.nlm.nih.gov/articles/PMC11489802/, accessed on March 8, 2026.
8. National Accreditation Board for Hospitals and Healthcare Providers. NABH standards. Available from: https://nabh.co/nabh-standards/, accessed on March 8, 2026.
9. World Health Organization. Ethics and governance of artificial intelligence for health. Geneva: WHO; 2021.
10. International Committee of Medical Journal Editors. Recommendations for the conduct, reporting, editing, and publication of scholarly work in medical journals. Available from: https://www.icmje.org/, accessed on March 8, 2026.
11. EQUATOR Network. Enhancing the quality and transparency of health research. Available from: https://www.equator-network.org/, accessed on March 8, 2026.
12. Indian Council of Medical Research. National ethical guidelines for biomedical and health research involving human participants. New Delhi: ICMR; 2017. Available from: https://www.icmr.gov.in/icmrobject/custom_data/pdf/resource-guidelines/ICMR_Ethical_Guidelines_2017.pdf, accessed on March 8, 2026.
13. World Health Organization. Progress on patient safety across health systems around the world. Available from: https://www.who.int/news/item/23-05-2025-progress-on-patient-safety-across-health-systems-around-the-world, accessed on March 8, 2026.
14. Garg S, Gangadharan N, Bhatnagar N, Singh MM, Raina SK, Galwankar S. The Ayushman Bharat Digital Mission of India: an assessment. J Med Syst 2024;48:123.
15. Leape LL. Reporting of adverse events. N Engl J Med 2002;347:1633-8.
16. Barach P, Small SD. Reporting and preventing medical mishaps: lessons from non-medical near miss reporting systems. BMJ 2000;320:759-63.
17. Pham JC, Girard T, Pronovost PJ. What to do with healthcare incident reporting systems. J Public Health Res 2013;2:e27.
18. Stavropoulou C, Doherty C, Tosey P. How effective are incident-reporting systems for improving patient safety? A systematic literature review. Milbank Q 2015;93:826-66.
19. Mitchell I, Schuster A, Smith K, Pronovost P, Wu A. Patient safety incident reporting: a qualitative study of thoughts and perceptions of experts 15 years after 'To Err is Human'. BMJ Qual Saf 2016;25:92-9.
20. Agency for Healthcare Research and Quality. Patient safety organizations and learning systems. Available from: https://www.ahrq.gov/patient-safety/reporting.html, accessed on March 8, 2026.
21. Bates DW, Singh H. Two decades since To Err Is Human: an assessment of progress and emerging priorities in patient safety. Health Aff 2018;37:1736-43.
22. Singh H, Sittig DF. Advancing the science of measurement of diagnostic errors in healthcare. BMJ Qual Saf 2015;24:103-10.
23. World Health Organization. World patient safety day 2024 campaign materials. Available from: https://www.who.int/campaigns/world-patient-safety-day/2024, accessed on March 8, 2026.
24. World Bank. India - transforming India’s public health surveillance through digital systems. Available from: https://documents1.worldbank.org/curated/en/099145106042242190/pdf/P175676001543d000b7c709870c0c3375b.pdf, accessed on March 8, 2026.
25. Flemons WW, McRae G. Reporting, learning and the culture of safety. Healthc Q 2012;15 Spec No:12-7.
