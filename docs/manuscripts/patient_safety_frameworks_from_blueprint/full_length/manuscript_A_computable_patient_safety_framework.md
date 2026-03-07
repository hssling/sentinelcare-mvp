# SentinelCare: A Computable Framework for Real-Time, Human-Governed Patient Safety Intelligence

## Title page

### Full title

SentinelCare: A Computable Framework for Real-Time, Human-Governed Patient Safety Intelligence

### Short title

Computable patient safety intelligence

### Authors

[Author names and affiliations to be inserted]

### Corresponding author

[Name, institution, email to be inserted]

## Abstract

### Background

Preventable harm in healthcare arises from distributed failures of timing, communication, sequencing, omission, and follow-up closure. Existing patient safety systems are often retrospective, fragmented across domains, and weakly integrated into real-time clinical workflow. As a result, many latent safety risks are identified too late to prevent harm, or are surfaced without clear ownership, escalation pathways, or closure tracking.

### Objective

To develop a comprehensive patient safety framework that makes safety risks computable, observable, actionable, and governable across heterogeneous healthcare processes.

### Methods

We performed a narrative-guided framework synthesis anchored in the SentinelCare founder blueprint and informed by current patient safety strategy, digital clinical decision support regulation, diagnostic safety literature, sepsis and deterioration guidelines, and evidence on medication safety and critical-result communication. Evidence and policy sources were mapped against a proposed multi-layer architecture and process-deviation model.

### Results

The resulting SentinelCare framework defines patient safety as a real-time control problem organized around the process chain Intent -> Action -> Confirmation -> Response -> Follow-up -> Closure. The framework specifies eight architectural layers, ten safety domains, explicit alert semantics, accountable role routing, escalation pathways, learning loops, and governance controls. It positions patient safety intelligence as a human-governed operational safety layer rather than autonomous diagnostic authority.

### Conclusions

SentinelCare offers a theoretically coherent and implementation-ready framework for prospective patient safety operations. It provides a foundation for staged validation and translational deployment across medication safety, critical-result closure, and deterioration surveillance pilots.

## Introduction

Patient safety remains a persistent global challenge despite decades of quality improvement, standardization efforts, and digital transformation. The World Health Organization (WHO) Global Patient Safety Action Plan 2021-2030 and the WHO Global Patient Safety Report 2024 emphasize that healthcare systems continue to generate significant preventable harm through complex system-level failures rather than isolated individual mistakes. In parallel, the National Action Plan to Advance Patient Safety in the United States argues that meaningful progress requires coordinated infrastructure for safety, learning, leadership, accountability, and patient-centered design. These policy directions highlight a structural gap: safety remains insufficiently computable in day-to-day clinical operations.

The prevailing patient safety ecosystem is still dominated by retrospective incident reporting, narrow quality dashboards, and siloed digital alerts. These tools can be useful, but they often fail to integrate the full set of data sources, workflow states, and human accountabilities needed to intervene before harm occurs. They also frequently separate technical prediction from operational response. In practice, this means that an abnormal signal may be detected without a clear owner, a due time, a follow-up chain, or a verified closure state. The effect is especially pronounced in medication management, diagnostic test follow-up, and clinical deterioration recognition, where avoidable delays and omissions remain common.

Meanwhile, the regulatory and governance environment around clinical decision support is maturing. The January 2026 revision of the U.S. Food and Drug Administration (FDA) Clinical Decision Support Software guidance further clarifies distinctions between non-device and device clinical decision support and reinforces expectations around transparency and intended use. FDA Good Machine Learning Practice principles and the Office of the National Coordinator for Health Information Technology (ONC) Decision Support Interventions transparency requirements similarly indicate that modern safety-oriented digital systems must make their logic, source attributes, and feedback pathways visible and governable. These developments make it increasingly difficult to justify opaque or poorly controlled safety automation.

The SentinelCare blueprint was conceived as a response to these converging needs. Rather than framing patient safety as a single predictive model or a dashboard category, the blueprint defines a layered safety intelligence platform that connects data ingestion, clinical knowledge, detection logic, prediction, intervention, learning, governance, and user experience into a unified operational safety architecture. It is explicitly designed as a human-in-the-loop system, prioritizing evidence-backed alerts, measurable impact, auditability, and site adaptability.

This manuscript presents a full-length framework paper derived from the SentinelCare blueprint and strengthened through current literature and guideline synthesis. The goal is not to claim completed prospective clinical effectiveness, but to articulate a rigorous theoretical and translational foundation for a multidomain patient safety intelligence platform. Specifically, we aim to answer three questions. First, how should patient safety be formalized as a computable control problem? Second, what architectural layers are necessary to connect risk detection with accountable action and learning? Third, how can such a system remain governable and human-centered while scaling across heterogeneous settings?

## Methods

### Study design

We used a framework-synthesis approach that combined blueprint-derived system specification with targeted literature and guideline review. The source blueprint was the founder design document for Project SentinelCare, which defined platform intent, safety domains, users, architecture, event models, governance requirements, and staged deployment priorities. The manuscript development process treated the blueprint as the primary design artifact and tested its internal structure against authoritative external sources.

### Literature and guidance review approach

The evidence review focused on five domains relevant to the framework:

1. global and national patient safety strategy,
2. diagnostic safety and closed-loop communication,
3. medication safety and computerized provider order entry/clinical decision support,
4. sepsis and deterioration surveillance,
5. AI and decision support governance.

Primary and official sources were prioritized wherever available. These included WHO patient safety publications, IHI National Action Plan materials, FDA guidance documents, ONC decision support intervention resources, peer-reviewed guideline statements, and high-impact peer-reviewed external validation studies. Supplementary review-level evidence was used to contextualize implementation risks and sociotechnical considerations when primary consensus documents were not sufficient.

The literature search and source verification were updated to March 7, 2026. Searches were performed for official guidance and primary papers relating to patient safety frameworks, test-result communication, computerized provider order entry and medication safety, sepsis surveillance, and AI/CDS regulation. Evidence was then mapped to design claims from the SentinelCare blueprint.

### Analytic framework

We evaluated the blueprint against three questions:

1. whether the safety problem is defined at the level of process control rather than isolated events,
2. whether the architecture supports accountable operational action after detection,
3. whether the design embeds governance and validation as runtime requirements rather than post hoc activities.

Findings were synthesized into a structured framework with explicit process primitives, architectural layers, operational invariants, and deployment implications.

## Results

### Safety as a computable process-control problem

The blueprint’s most important conceptual move is to define clinical safety in process terms rather than solely in outcome or incident terms. SentinelCare represents every clinical pathway as a chain:

Intent -> Action -> Confirmation -> Response -> Follow-up -> Closure

This formulation is not merely descriptive. It creates a shared safety grammar for heterogeneous clinical domains. A safety event can be operationally recognized when one or more of the following occur:

1. an expected action is missing,
2. evidence sources contradict each other,
3. a time threshold for safe action is exceeded,
4. ownership is ambiguous or absent,
5. closure is not achieved despite signal acknowledgement.

This process logic aligns with broader patient safety thinking in which preventable harm is produced by system conditions, coordination failures, and weak recovery structures. It also addresses a known gap in digital decision support, where alerts are often generated without embedding the later stages of ownership and closure.

### Eight-layer architecture for operational safety intelligence

The framework synthesizes the blueprint into eight linked layers.

Layer 1, the Data Fabric, establishes input reliability through healthcare interoperability connectors, event normalization, identity resolution, terminology mapping, and time synchronization. This layer addresses a core practical barrier to real-time safety systems: signal fragmentation and inconsistent semantics across source systems.

Layer 2, the Clinical Knowledge Layer, transforms guidelines, standard operating procedures, formulary constraints, contraindication logic, escalation rules, and checklists into computable policy artifacts. This makes local governance possible without hard-coding all site-specific variation into analytic logic.

Layer 3, the Detection Layer, contains deterministic rule engines, process deviation logic, contradiction detection, and multimodal extraction. This layer is central to the MVP because it provides interpretable, auditable baseline signal generation before broader predictive expansion.

Layer 4, the Prediction Layer, extends from detection to anticipatory risk modeling. In the blueprint this includes deterioration models, adverse drug event risk models, missed follow-up models, diagnostic delay models, and operational risk forecasts. Prediction is not treated as sufficient by itself; it is upstream of intervention and governance.

Layer 5, the Intervention Layer, converts signal into workflow. It includes silent watchlists, soft alerts, interruptive alerts, escalation workflows, checklist launchers, and one-click corrective actions. This layer distinguishes SentinelCare from dashboard-only systems by requiring actionability and owner assignment.

Layer 6, the Learning Layer, captures feedback, overrides, false-positive and false-negative review, and site drift. This supports continual improvement while preserving local operating context.

Layer 7, the Governance Layer, includes model and policy version control, approval workflows, audit logs, explainability stores, and rollback or kill-switch capability. In the framework, governance is not optional overhead; it is a safety function.

Layer 8, the Experience Layer, provides role-specific user interfaces and command views. Its function is not cosmetic. It makes the hidden logic of safety operations visible to clinicians, quality teams, and administrators.

### Multidomain structure with narrow-first deployment

The blueprint defines ten safety domains: medication safety, diagnostic safety, procedure/surgical safety, deterioration surveillance, infection prevention and environmental safety, laboratory/radiology process safety, care transition safety, documentation/communication safety, device/equipment safety, and operational safety. This breadth is architecturally important because it prevents the system from being overfitted to a single problem class.

At the same time, the blueprint explicitly rejects broad simultaneous deployment. It narrows the first deployable version to three measurable pilots:

1. medication safety,
2. critical-result follow-up safety,
3. deterioration/sepsis/shock surveillance.

This narrow-first strategy is consistent with implementation science and patient safety practice. It acknowledges that broad architectural ambition should not be confused with broad operational launch. Instead, a stable multidomain substrate is built first, then deployed selectively where measurement and governance are strongest.

### Human governance as an architectural invariant

The framework consistently positions human oversight as a default requirement. This is reinforced in the product principles, governance requirements, and validation plan. High-risk decisions require human review. Alerts must be evidence-backed. Override capture must be logged. Site-specific governance must be supported without breaking global control.

This design aligns with current regulatory direction. FDA CDS guidance stresses intended use and transparency boundaries; ONC DSI criteria require source attribute visibility and structured feedback capability; GMLP principles reinforce lifecycle controls. SentinelCare translates those expectations into architecture rather than leaving them as compliance annotations.

### Measurable operational metrics

The framework yields a coherent outcome and process metric set. Instead of relying only on aggregate harm reduction claims, it emphasizes:

1. positive predictive value,
2. sensitivity for selected safety events,
3. median time-to-detection,
4. median time-to-acknowledgment,
5. median time-to-corrective-action,
6. override rate,
7. harmful false-positive rate,
8. no-action-after-alert rate,
9. harm per 1,000 encounters in pilot domains,
10. clinician trust score.

These metrics support staged translational validation rather than premature effectiveness claims.

## Discussion

This framework paper advances a view of patient safety intelligence that is broader than algorithm performance and narrower than unconstrained “AI transformation” narratives. SentinelCare’s central contribution is architectural: it defines a way to make safety computable without detaching detection from workflow, accountability, and governance.

Several features distinguish the framework from common digital health patterns. First, it treats safety as a process-control problem rather than a document-mining or single-score problem. This matters because preventable harm often emerges not from one missed fact but from incomplete action chains. Second, it embeds operational response in the same structure as detection, which reduces the common failure mode of alerting without closure. Third, it treats governance and learning as runtime features, enabling safer scale-up and adaptation.

The framework also clarifies what SentinelCare is not. It is not a monolithic autonomous medical decision-maker. It is not a replacement for clinician judgment. It is not a single predictive model wrapped in a dashboard. Rather, it is a prospective safety layer designed to surface deviations, support intervention, and preserve human accountability.

This framing is especially important in light of evidence from real-world clinical AI. External validation of widely implemented proprietary sepsis prediction models has shown that performance can degrade substantially outside development settings. That experience underscores the importance of staged validation, local calibration, and governance before clinical reliance. SentinelCare’s architecture is compatible with ML-enabled prediction, but it does not require trust in prediction alone to produce value.

The present work has limitations. It is a framework synthesis grounded in a blueprint and literature review, not a completed prospective outcomes study. It therefore cannot yet claim reduction in patient harm in live clinical operations. In addition, some aspects of the architecture, such as multimodal extraction and enterprise-grade interoperability, remain translational components requiring site-specific implementation. Nonetheless, the theoretical and systems structure is strong enough to guide immediate pilot design, governance planning, and manuscript development.

The next translational step should be controlled implementation in narrow pilot domains with retrospective benchmarking followed by silent prospective validation. This progression is both clinically safer and scientifically stronger than direct live rollout.

## Conclusion

SentinelCare provides a coherent, layered, and governable framework for real-time patient safety intelligence. By formalizing safety as a computable process-control problem and linking detection to escalation, closure, learning, and governance, it establishes a strong theoretical base for prospective patient safety systems. The framework supports staged translation from conceptual architecture to measurable pilot deployment in medication safety, critical-result closure, and deterioration surveillance.

## Declarations

### Ethics approval and consent to participate

Not applicable for this framework manuscript. No human participant dataset was analyzed for the present paper.

### Consent for publication

Not applicable.

### Data availability

No patient-level dataset is reported in this manuscript. Framework source materials are contained in the project repository and associated blueprint documentation.

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
5. U.S. Food and Drug Administration. Clinical Decision Support Software: Guidance for Industry and Food and Drug Administration Staff. January 2026. Available from: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software
6. U.S. Food and Drug Administration. Good Machine Learning Practice for Medical Device Development: Guiding Principles. Available from: https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles
7. Office of the National Coordinator for Health Information Technology. Decision support interventions. Available from: https://www.healthit.gov/test-method/decision-support-interventions
8. Evans L, Rhodes A, Alhazzani W, et al. Surviving sepsis campaign: international guidelines for management of sepsis and septic shock 2021. Crit Care Med. 2021. Available from: https://pubmed.ncbi.nlm.nih.gov/34599691/
9. Wong A, Otles E, Donnelly JP, et al. External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. JAMA Intern Med. 2021. Available from: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307
10. Apalodimas L, Peiffer-Smadja N, et al. External validation in county emergency departments of a widely implemented sepsis model. JAMIA Open. 2024. Available from: https://pubmed.ncbi.nlm.nih.gov/39545248/
11. Callen J, Georgiou A, Li J, Westbrook JI. Closing the loop on test results to reduce communication failures: a rapid review of evidence, practice and patient perspectives. BMC Health Serv Res. 2020. Available from: https://pmc.ncbi.nlm.nih.gov/articles/PMC7510293/

