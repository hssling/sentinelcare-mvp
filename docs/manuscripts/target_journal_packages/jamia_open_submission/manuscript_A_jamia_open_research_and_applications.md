# SentinelCare: A computable framework for real-time, human-governed patient safety intelligence

## Structured Abstract

### Objectives

To develop and specify a computable, multidomain patient safety framework that links heterogeneous clinical data, explicit safety logic, human accountability, and governance into a real-time operational safety system.

### Materials and Methods

We performed a blueprint-centered framework synthesis using the SentinelCare founder blueprint as the primary design artifact and tested its assumptions against current patient safety strategy, clinical decision support regulation, diagnostic safety literature, medication safety evidence, and sepsis and deterioration guidance. We then translated the resulting framework into a staged informatics architecture, domain taxonomy, runtime control model, and formative prototype package aligned to narrow pilot domains.

### Results

The resulting framework defines patient safety as a process-control problem organized around the chain `intent -> action -> confirmation -> response -> follow-up -> closure`. It specifies eight architectural layers, ten safety domains, three near-term pilot domains, explicit alert semantics, accountable routing rules, governance controls, and a validation pathway. The design positions digital safety intelligence as a human-governed operational layer rather than an autonomous diagnostic agent. It also yields a measurable evaluation framework spanning timeliness, alert burden, override behavior, escalation performance, and downstream harm-related outcomes.

### Discussion

SentinelCare addresses a common failure of digital safety systems: they often detect risk without guaranteeing ownership, escalation, or verified closure. By making those downstream operational states first-class design objects, the framework aligns with current WHO, IHI, FDA, ONC, diagnostic safety, and sepsis guidance. It also improves on narrow domain-specific tools by offering a common control structure that can scale across medication safety, critical-result follow-up, and deterioration surveillance.

### Conclusion

SentinelCare provides a publication-ready and implementation-oriented framework for prospective patient safety operations. It supports immediate narrow-domain pilots and offers a coherent basis for later empirical validation, governance maturation, and broader clinical deployment.

## Background and Significance

Preventable harm remains a major systems problem across modern healthcare. The World Health Organization (WHO) Global Patient Safety Action Plan 2021-2030 and the WHO Global Patient Safety Report 2024 both argue that patient safety failures are produced by interacting system weaknesses rather than isolated clinician mistakes.[1,2] The United States National Action Plan to Advance Patient Safety similarly emphasizes the need for coordinated infrastructure for leadership, culture, learning, patient engagement, and safer care delivery.[3] These policy documents converge on the same operational problem: most health systems still do not have a reliable real-time mechanism for detecting, routing, governing, and learning from safety threats as care unfolds.

Existing digital patient safety tools are often fragmented. Incident reporting systems are retrospective. Quality dashboards aggregate lagging indicators. Alerting systems frequently operate inside single workflows without preserving ownership across downstream steps. Domain-specific applications, such as medication alerts, sepsis screens, or radiology notification tools, can provide value but rarely share a common representation of what constitutes a safety failure, what constitutes closure, who owns the next action, and how the system should learn over time. This fragmentation weakens the operational chain needed to prevent harm.

Several evidence streams reinforce the need for a more rigorous design foundation. First, diagnostic safety literature has shown that failure to close the loop on test results remains an important and persistent source of delayed or missed diagnosis.[4,5] Second, medication-related clinical decision support (CDS) can reduce harm but frequently suffers from poor specificity, high override rates, and alert fatigue when workflow and human factors are not properly addressed.[6-8] Third, deterioration and sepsis surveillance require timeliness and accountable escalation; however, real-world external validations of widely implemented sepsis models have shown performance degradation and context sensitivity across sites, underscoring the limits of treating prediction alone as safety infrastructure.[9-12]

At the same time, regulatory expectations for safety-oriented digital systems have become sharper. The January 2026 revision of the US Food and Drug Administration (FDA) Clinical Decision Support Software guidance further clarifies the distinction between device and non-device CDS and emphasizes intended use, transparency, and the role of clinician review.[13] FDA Good Machine Learning Practice (GMLP) principles reinforce lifecycle controls for high-risk software.[14] The Office of the National Coordinator for Health Information Technology (ONC) Decision Support Interventions requirements emphasize source attribution, transparency of intervention logic, and feedback pathways within certified health IT.[15] Together, these documents indicate that future patient safety systems will need not only analytic capability, but also explainability, version control, human governance, and measurable operational performance.

SentinelCare was conceived to address this gap. The project blueprint describes a multidomain patient safety intelligence platform intended to convert patient safety from a retrospective reporting activity into a prospective operational control layer. Instead of framing safety as a collection of unrelated alerts, the blueprint defines a common process grammar, a layered architecture, domain-specific safety programs, explicit routing rules, and governance primitives that can be implemented incrementally. The blueprint is ambitious, but its architectural value lies in the combination of breadth and narrow-first deployment logic: it supports many domains while recommending that initial live implementation focus on the domains where signal definition, measurement, and intervention workflows are strongest.

This manuscript presents the blueprint-derived framework in a format suitable for clinical informatics evaluation and staged translation. It is not a claim of completed prospective effectiveness testing. Rather, it specifies the theoretical, architectural, and operational basis for a real-time patient safety system that is explainable, governable, and implementable.

## Objectives

This study had four objectives:

1. to formalize patient safety as a computable process-control problem rather than a purely retrospective event classification problem;
2. to derive a multidomain architecture that connects detection, intervention, learning, and governance within a single operational framework;
3. to align that architecture against contemporary patient safety, CDS, diagnostic safety, and deterioration-management guidance; and
4. to define a translational deployment and validation pathway for early SentinelCare pilots.

## Materials and Methods

### Design

We used a framework-synthesis design. The SentinelCare founder blueprint served as the primary design artifact. That artifact described system intent, architecture, actors, deployment stages, safety domains, governance requirements, and product principles. We treated the blueprint not as finished evidence, but as a candidate systems theory to be pressure-tested against established external literature and guidance.

### Source selection and review approach

We conducted a targeted, source-prioritized literature and guidance review updated to March 7, 2026. Primary and official sources were prioritized over secondary commentary. Five evidence blocks were assembled:

1. systems-level patient safety strategy and organizational safety frameworks;
2. diagnostic safety and closed-loop test-result communication;
3. medication safety and computerized provider order entry/CDS evidence;
4. deterioration and sepsis recognition, escalation, and implementation studies; and
5. CDS, AI, and software governance guidance relevant to transparency, lifecycle controls, and operational oversight.

Evidence was considered relevant when it informed one of four design questions: what constitutes a safety-relevant deviation, what operational response is required after detection, what risks emerge when alerting is not governable, and what conditions are necessary for translational validation. Official sources included WHO, IHI, FDA, ONC, and Joint Commission materials.[1-3,13-16] Peer-reviewed primary studies and reviews were used to test whether blueprint assumptions were aligned with known implementation realities.[5-12,17-20]

### Analytic procedure

The blueprint was decomposed into process primitives, architectural layers, domain programs, governance functions, and deployment stages. Each component was then mapped against the external evidence blocks. Components were retained if they were coherent with the evidence base, modified if the literature identified implementation or safety risks, and deprioritized if they lacked an actionable translational path.

Three analytic criteria were applied:

1. `Process completeness`: whether a design element addressed not only detection, but also accountable action, escalation, and closure.
2. `Sociotechnical plausibility`: whether the design recognized workflow, alert burden, accountability, data quality, and implementation variation.
3. `Governability`: whether the design could support policy versioning, explainability, audit, validation, and rollback.

### Translational prototype linkage

To test whether the resulting framework could be operationalized, we linked the framework to the current SentinelCare prototype. The prototype includes staged multi-agent workflow orchestration, domain-specific rule engines, queueing and escalation structures, policy-governance objects, validation-report endpoints, Supabase-backed persistence, and a demonstration interface. These prototype components were not treated as definitive effectiveness evidence; instead, they were used as formative proof that the framework can be encoded into working software objects and runtime workflows.

## Results

### A computable safety grammar

The most important outcome of the synthesis was a common control grammar for patient safety. SentinelCare represents clinical safety processes as a chain:

`intent -> action -> confirmation -> response -> follow-up -> closure`

The framework defines a safety deviation as any state in which one or more of the following conditions occurs:

1. an expected clinical or operational action does not occur;
2. data sources are contradictory in a clinically meaningful way;
3. a safety-relevant time threshold is exceeded;
4. ownership of the next action is ambiguous or absent; or
5. acknowledgement occurs without verified closure.

This model improves on conventional event-centric safety design because it makes failures of timing, sequencing, and accountability computable across domains rather than treating them as narrative exceptions. The model is compatible with both deterministic logic and predictive analytics, but it does not depend on prediction to function.

### Eight-layer architecture

The framework resolves the blueprint into eight operational layers (Table 1, Figure 1).

1. `Data fabric`: interoperability connectors, event normalization, identity resolution, terminology mapping, and time synchronization.
2. `Clinical knowledge`: computable policies derived from guidelines, formulary rules, escalation rules, and local protocols.
3. `Detection`: deterministic rule engines, contradiction checks, process-deviation logic, and structured extraction.
4. `Prediction`: temporal risk estimation for deterioration, missed follow-up, adverse drug events, and workflow failure.
5. `Intervention`: watchlists, alerts, checklists, task generation, routing, and escalation.
6. `Learning`: override capture, false-positive and false-negative review, drift review, and local tuning.
7. `Governance`: approval workflows, versioning, explainability artifacts, audit logs, and rollback controls.
8. `Experience`: role-specific user interfaces for clinicians, pharmacists, quality leaders, and operations teams.

This architecture matters because most digital safety systems stop at layers 2-4. SentinelCare explicitly includes layers 5-8 as design requirements. That shifts the system from passive alert production to accountable safety operations.

### Ten-domain model with narrow-first pilots

The framework preserves the blueprint's broad domain scope while explicitly constraining early deployment. Ten domains are represented: medication safety, diagnostic safety, procedure and surgical safety, deterioration surveillance, infection and environmental safety, laboratory and radiology process safety, care transition safety, documentation and communication safety, device and equipment safety, and operational safety.

However, the framework identifies three domains for immediate translational pilots:

1. `medication safety`, because computable contraindications, duplicate therapy, and dose-adjustment rules are relatively mature;
2. `critical-result follow-up`, because closed-loop communication failures are common, measurable, and operationally actionable; and
3. `deterioration surveillance`, including sepsis and shock pathways, because timeliness and escalation can be measured prospectively.

This narrow-first strategy is central to the framework's practicality. It permits the architecture to remain multidomain while avoiding the implementation error of trying to operationalize every patient safety domain simultaneously.

### Human-governed alert semantics and routing

The synthesis also produced explicit alert semantics. Alerts are not treated as uniform notifications. They are categorized by urgency, interruptiveness, recommended action type, required role, expected response time, and closure evidence. Within the prototype, this logic is encoded through queue items, escalation levels, and review actions. Conceptually, it establishes that a safety alert is incomplete until the system can answer five questions: what happened, why it matters, who owns the next action, by when, and what constitutes closure.

This design responds directly to known deficiencies in medication and result-management alerting, where excessive alert volume and weak ownership can produce acknowledgement without meaningful action.[5-8] It also aligns with Joint Commission emphasis on timely communication and responsible follow-up of critical test results.[16]

### Governance and validation as runtime functions

The framework does not treat governance as a post hoc committee task. Instead, policy versioning, approval states, validation reports, audit logs, and override review are runtime components. This is an important distinction. For patient safety systems, the question is not only whether an algorithm can identify risk, but whether the surrounding system can prove what logic was active, who approved it, how performance is monitored, and how a problematic rule or model can be withdrawn.

This choice aligns with FDA and ONC guidance on transparency and lifecycle control.[13-15] It also addresses lessons from real-world sepsis model deployment, where transportability and local performance variability make predeployment claims insufficient.[9-12]

### A measurable translational evaluation framework

The synthesis produced a staged evaluation model (Table 4, Figure 3). Core measures include:

1. positive predictive value;
2. domain-specific sensitivity or event capture rate;
3. median time to detection;
4. median time to acknowledgement;
5. median time to corrective action;
6. escalation completion rate;
7. override rate and override appropriateness;
8. no-action-after-alert rate;
9. queue overdue burden; and
10. pilot-domain harm indicators per 1000 encounters.

This measurement set supports three phases: retrospective rule and cohort validation, silent-mode prospective evaluation, and controlled intervention deployment. The framework therefore gives sites a concrete pathway from concept to operational learning without forcing an unsafe or scientifically weak immediate live rollout.

## Discussion

This work translates the SentinelCare blueprint into a computable patient safety framework suited to informatics implementation and evaluation. Its main contribution is not a single predictive algorithm. Its contribution is architectural: it unifies data, knowledge, detection, workflow, learning, and governance within a common control structure that is general enough to span multiple safety domains and narrow enough to support realistic early pilots.

Three elements distinguish the framework from many existing digital safety tools.

First, it treats patient safety as a process-control problem. That matters because preventable harm often arises from incomplete chains of care rather than isolated abnormal values. A critical laboratory result becomes dangerous not because the value exists, but because acknowledgement, communication, or action fails. A medication order becomes dangerous not simply because it matches a rule, but because a contraindication is missed, routed poorly, or overridden inappropriately. A deterioration pathway becomes dangerous not just when risk rises, but when a timely response does not occur. By explicitly modeling those process states, SentinelCare broadens what can be made computable.

Second, the framework insists that detection without accountable action is an incomplete design. This position is strongly supported by the literature. Closed-loop test-result reviews emphasize responsibility, timely notification, and closure verification.[5] Medication CDS evidence repeatedly shows that large alert volumes without careful targeting lead to alert fatigue and override behavior.[6-8] External sepsis-model validations show that raw predictive performance alone cannot justify reliance without local operational controls and monitoring.[9-12] The framework addresses these issues by embedding owner routing, due times, escalation paths, and closure requirements directly into its design objects.

Third, the framework places governance inside the operating model. This is both a practical and ethical requirement. The closer a system gets to influencing urgent clinical workflows, the less acceptable it becomes to run opaque logic without version control, source attribution, validation reports, and kill-switch capability. The framework's governance layer therefore serves not only institutional oversight but also direct clinical safety.

The framework also improves on simple "AI for patient safety" narratives by making the role boundaries explicit. SentinelCare is not designed as an autonomous diagnostic authority. It is a human-governed safety intelligence layer. In this respect, it is better understood as an operational control system than as a stand-alone AI model. That distinction matters for regulatory alignment, implementation strategy, and clinician trust.

There are limitations. This manuscript is a framework and translational design paper, not a completed prospective clinical effectiveness study. The prototype demonstrates implementability, not clinical benefit. In addition, broad architectural scope always risks conceptual overreach if governance, integration, and pilot sequencing are weak. We addressed that risk by prioritizing narrow pilot domains, explicit validation phases, and a governance-first architecture. Even so, site-specific implementation work remains substantial, especially for interoperability, role-directory integration, formulary customization, workflow mapping, and prospective evaluation design.

The next logical research steps are concrete. First, the medication safety, critical-result closure, and deterioration pilots should undergo retrospective benchmarking with site-level chart review and process validation. Second, silent-mode deployment should quantify alert burden, timeliness, and missed-event patterns before any interruptive action is introduced. Third, intervention-stage evaluations should test whether the framework improves time to acknowledgement, time to corrective action, and selected harm-related process outcomes without unacceptable alert burden. Only after those steps should broader multidomain scale-up be attempted.

## Conclusion

SentinelCare offers a coherent, governable, and implementation-ready framework for real-time patient safety intelligence. By defining safety as a computable process-control problem and by integrating detection with routing, escalation, closure, learning, and governance, the framework improves on fragmented digital safety approaches that stop at signal generation. The resulting architecture is aligned with current patient safety strategy and CDS governance expectations and provides a defensible basis for staged translational deployment in medication safety, critical-result follow-up, and deterioration surveillance.

## Funding

No specific external funding was received for this framework development, manuscript preparation, or prototype implementation work.

## Acknowledgments

The authors acknowledge the blueprint development work, implementation prototyping, and literature synthesis efforts that informed the SentinelCare framework.

If applicable at submission, include an AI-use disclosure consistent with journal policy, for example: "The authors used generative AI assistance for drafting support and language editing under direct human supervision. All factual assertions, references, interpretations, and final manuscript text were reviewed and verified by the authors."

## Conflict of Interest

Dr. Siddalingaiah H S is the lead architect and maintainer of the SentinelCare concept, manuscripts, and prototype repository. No commercial product revenue is reported for the work described in this manuscript.

## Data Availability

No patient-level dataset is reported in this framework paper. Non-sensitive project materials, prototype artifacts, and code are available in the public repository: https://github.com/hssling/sentinelcare-mvp

## References

1. World Health Organization. Global patient safety action plan 2021-2030: towards eliminating avoidable harm in health care. Geneva, Switzerland: World Health Organization; 2021.
2. World Health Organization. Global patient safety report 2024. Geneva, Switzerland: World Health Organization; 2024.
3. Institute for Healthcare Improvement. Safer together: a national action plan to advance patient safety. Boston, MA: IHI; 2022.
4. National Academies of Sciences, Engineering, and Medicine. Improving diagnosis in health care. Washington, DC: The National Academies Press; 2015.
5. Callen J, Georgiou A, Li J, Westbrook JI. Closing the loop on test results to reduce communication failures: a rapid review of evidence, practice and patient perspectives. BMC Health Serv Res. 2020;20:897.
6. Kwan JL, Lo L, Ferguson J, et al. Computerised clinical decision support systems and absolute improvements in care: meta-analysis of controlled clinical trials. BMJ. 2020;370:m3216.
7. Slight SP, Beeler PE, Seger DL, et al. A cross-sectional observational study of high override rates of drug allergy alerts in inpatient and outpatient settings, and opportunities for improvement. BMJ Qual Saf. 2017;26(3):217-225.
8. Nanji KC, Seger DL, Slight SP, et al. Medication-related clinical decision support alert overrides in inpatients. J Am Med Inform Assoc. 2018;25(5):476-481.
9. Evans L, Rhodes A, Alhazzani W, et al. Surviving sepsis campaign: international guidelines for management of sepsis and septic shock 2021. Crit Care Med. 2021;49(11):e1063-e1143.
10. Wong A, Otles E, Donnelly JP, et al. External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. JAMA Intern Med. 2021;181(8):1065-1070.
11. Apalodimas L, Meyer AN, Ali T, et al. External validation in county emergency departments of a widely implemented sepsis prediction model. JAMIA Open. 2024;7(4):ooae116.
12. Choi JH, Kim J, Kim J, et al. Real-time machine learning-assisted sepsis alert enhances the timeliness of antibiotic administration and diagnostic accuracy in emergency department patients with sepsis: a cluster-randomized trial. npj Digit Med. 2024;7:52.
13. US Food and Drug Administration. Clinical decision support software: guidance for industry and Food and Drug Administration staff. Silver Spring, MD: FDA; January 2026.
14. US Food and Drug Administration, Health Canada, Medicines and Healthcare products Regulatory Agency. Good machine learning practice for medical device development: guiding principles. Silver Spring, MD: FDA; 2021.
15. Office of the National Coordinator for Health Information Technology. Decision support interventions. Washington, DC: ONC Health IT Certification Program; accessed March 7, 2026.
16. The Joint Commission. National patient safety goals and critical test result communication standards and FAQs. Oakbrook Terrace, IL: The Joint Commission; accessed March 7, 2026.
17. Singh H, Sittig DF. A sociotechnical framework for safety-related electronic health record research reporting: the SAFER reporting framework. Ann Intern Med. 2020;172(11 Suppl):S92-S100.
18. Sittig DF, Singh H. A new sociotechnical model for studying health information technology in complex adaptive healthcare systems. Qual Saf Health Care. 2010;19 Suppl 3:i68-i74.
19. Bates DW, Kuperman GJ, Wang S, et al. Ten commandments for effective clinical decision support: making the practice of evidence-based medicine a reality. J Am Med Inform Assoc. 2003;10(6):523-530.
20. Richardson S, Lawrence K, Schoen M, Myers D. One size does not fit all: understanding user preferences for design of medication decision support. Appl Clin Inform. 2012;3(2):166-173.
