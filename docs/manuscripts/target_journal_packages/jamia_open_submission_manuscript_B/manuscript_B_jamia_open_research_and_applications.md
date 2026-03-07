# A unified domain taxonomy and process-deviation framework for multidomain patient safety intelligence

## Structured Abstract

### Objectives

To develop a multidomain patient safety taxonomy and process-deviation framework that supports prospective detection, comparable alert semantics, accountable routing, and cross-domain evaluation across heterogeneous clinical safety programs.

### Materials and Methods

We performed a blueprint-centered framework synthesis using the SentinelCare founder blueprint as the primary design source and tested the resulting domain structure against patient safety strategy, diagnostic safety literature, medication safety CDS evidence, deterioration-management guidance, and systems-safety concepts from clinical informatics. Domain categories and process-deviation classes were iteratively refined to preserve both clinical specificity and cross-domain comparability.

### Results

The resulting framework specifies 10 patient safety domains and a shared deviation grammar consisting of omission, contradiction, harmful delay, sequencing mismatch, and closure failure. It also defines a common alert schema requiring evidence, responsible owner, action deadline, recommended response, and override policy. The framework supports standardized cross-domain measures including time to detection, time to acknowledgement, time to action, closure completion, override rate, no-action-after-alert rate, and harmful false-positive rate.

### Discussion

This framework addresses a structural limitation in many safety technologies: domains are often digitized as isolated point solutions rather than as parts of a common operational substrate. By standardizing workflow deviation rather than clinical content, the model supports multidomain scale-up without flattening local meaning. It also improves implementation tractability by enabling one event model, one queueing logic, and one governance structure across safety domains.

### Conclusion

A unified domain taxonomy and process-deviation framework provides the conceptual infrastructure required for scalable patient safety intelligence and offers a defensible basis for staged multidomain deployment.

## Background and Significance

Patient safety programs operate across diverse hazards, yet digital tooling remains fragmented. Medication safety, diagnostic follow-up, deterioration surveillance, procedure safety, care transitions, documentation quality, device events, and operational failures are commonly addressed through separate systems, separate taxonomies, and separate governance processes. This fragmentation produces predictable consequences: duplicated infrastructure, inconsistent severity logic, weak cross-domain comparability, and limited ability to build a coherent safety operations layer.

The challenge is partly semantic. A broad patient safety system cannot simply aggregate alerts from unrelated point solutions, because domains differ in clinical content, signal sources, and response pathways. At the same time, if every domain is represented with its own independent event semantics, a multidomain platform becomes brittle and difficult to govern. A common representation is therefore needed, but it must preserve local clinical meaning and operational usefulness.

This problem is visible across several evidence domains. Diagnostic safety work has emphasized failures in follow-up, communication, and closure rather than isolated test abnormalities.[1,2] Medication CDS literature has shown that technically correct signals still fail when alert semantics, ownership, and override handling are weak.[3-5] Deterioration and sepsis literature highlights timeliness and escalation rather than pure classification alone.[6,7] Systems-level safety strategy from WHO and IHI further suggests that scalable patient safety work requires shared learning structures, accountability, and operational discipline across hazards.[8-10]

The SentinelCare blueprint addresses this problem by defining both a broad domain taxonomy and a common process representation based on `intent -> action -> confirmation -> response -> follow-up -> closure`. The core insight is that safety domains differ primarily in their clinical content, whereas many operational failures share common process forms. If that proposition is correct, a scalable patient safety platform can standardize around workflow deviation while allowing local rules and triggers to remain domain-specific.

This manuscript develops that proposition into a formal multidomain taxonomy and process-deviation framework suitable for informatics implementation, governance, and staged evaluation.

## Objectives

This study had four objectives:

1. to define a clinically credible multidomain patient safety taxonomy suitable for platform design;
2. to derive a small set of process-deviation classes that can generalize across domains;
3. to specify the minimum common alert semantics required for accountable safety operations; and
4. to identify cross-domain measures that allow comparable evaluation without sacrificing domain-specific meaning.
## Materials and Methods

### Design source

The SentinelCare founder blueprint served as the primary design artifact. It specified domain programs, alert behavior, process states, event semantics, governance requirements, and staged deployment logic. We extracted the domain model and process logic from that blueprint and treated them as candidate components of a shared safety taxonomy.

### Evidence review strategy

We conducted a targeted framework review updated to March 7, 2026, focusing on evidence areas where cross-domain representation is especially challenging:

1. medication safety and alert fatigue;
2. diagnostic safety and test-result closure;
3. deterioration recognition and escalation;
4. workflow reliability and communication failure; and
5. systems-level patient safety strategy.

The review prioritized official frameworks and primary literature. The purpose was not to exhaustively review every clinical safety domain, but to determine whether the proposed taxonomy could support a common operational language across high-priority use cases.

### Analytic approach

We applied a three-step synthesis:

1. retain the blueprint's broad domain taxonomy;
2. abstract deviation types from the common care-process chain;
3. test whether each domain could be represented using the same limited deviation set without loss of operational clarity.

A candidate deviation class was retained if it met three conditions:

1. it could be instantiated in more than one safety domain;
2. it corresponded to an actionable workflow failure; and
3. it supported a clear downstream response and closure definition.

### Prototype linkage

We also evaluated whether the resulting semantics could be encoded in the existing SentinelCare prototype. The prototype currently includes domain-specific rule engines, common alert objects, queue items, escalation structures, and review actions. This linkage was used as formative implementation support, not as effectiveness evidence.

## Results

### Ten-domain patient safety taxonomy

The resulting taxonomy retains 10 domains:

1. medication safety;
2. diagnostic safety;
3. procedure and surgical safety;
4. deterioration surveillance;
5. infection prevention and environmental safety;
6. laboratory and radiology process safety;
7. care transition safety;
8. documentation and communication safety;
9. device and equipment safety; and
10. operational safety.

This structure is broad enough to represent major hospital and ambulatory safety problems while remaining operationally interpretable to governance and implementation teams. It also reflects the fact that a single patient episode can move across multiple safety domains in a short time window.

### Shared process-deviation grammar

The central result is a compact deviation grammar consisting of 5 classes:

1. `omission`;
2. `contradiction`;
3. `harmful delay`;
4. `sequencing mismatch`; and
5. `closure failure`.

`Omission` captures missing expected actions such as absent renal dose adjustment, missed bedside reassessment, or omitted discharge follow-up. `Contradiction` captures clinically relevant discordance across sources, such as an allergy-linked medication order or a documented plan that conflicts with radiology findings. `Harmful delay` captures time-threshold breaches, including delayed critical-result acknowledgement and delayed deterioration escalation. `Sequencing mismatch` captures unsafe order of operations, such as downstream tasks occurring before prerequisite confirmation. `Closure failure` captures unresolved pathways despite acknowledgement or partial action.

### Domain-specific instantiation

The same deviation classes can be instantiated across domains while preserving local meaning.

In medication safety, omission includes failure to perform dose adjustment or medication reconciliation. Contradiction includes drug-allergy conflicts and therapeutic duplication. Closure failure includes unresolved reconciliation discrepancies at transition points.

In diagnostic safety and laboratory or radiology process safety, harmful delay and closure failure are especially important. Critical findings may be transmitted but not acknowledged, acknowledged but not acted on, or acted on without documented completion of the intended diagnostic pathway.

In deterioration surveillance, omission and harmful delay predominate. Rising-risk patterns may not trigger escalation, sepsis bundle elements may remain incomplete, or reassessment may occur too late to preserve the intended safety window.

In care transitions, closure failure becomes a major organizing class, encompassing referral leakage, discharge communication gaps, unresolved medication issues, and missing follow-up actions.

### Common alert semantics

A major consequence of the taxonomy is that all domains can operate through a common alert schema. Each actionable alert should minimally specify:

1. the reason the alert fired;
2. the evidence supporting the alert;
3. the responsible owner or role;
4. the deadline or expected response interval;
5. the recommended action; and
6. the override policy and documentation requirement.

These semantics are not just engineering conveniences. They are the minimum requirements for accountable operational response across diverse hazards.

### Cross-domain metric framework

The framework supports standardized measures across domains:

1. time to detection;
2. time to acknowledgement;
3. time to action;
4. closure completion rate;
5. override rate;
6. no-action-after-alert rate; and
7. harmful false-positive rate.

These platform-level measures can sit alongside domain-specific outcomes and are more informative than raw alert counts for assessing whether patient safety operations are actually improving.
## Discussion

A multidomain safety intelligence platform requires a durable semantic substrate. Without one, every domain becomes a custom point solution with its own event model, action logic, severity labels, and review process. That fragmentation does not scale. Conversely, excessive abstraction produces a safety language that is formally tidy but clinically unusable. The framework presented here addresses that tension by standardizing workflow deviation rather than clinical content.

This choice has several advantages. First, it preserves domain specificity. A harmful delay in critical-result follow-up is clinically different from a harmful delay in sepsis escalation, but both can be treated as the same class of operational failure. Second, it improves implementation efficiency. One event fabric, one queueing model, one alert object, and one governance model can serve multiple domains. Third, it improves user experience because downstream action semantics remain consistent even when clinical triggers differ.

The approach is also aligned with broader sociotechnical thinking in health IT safety. Sittig and Singh's sociotechnical model and related EHR safety frameworks emphasize that safe digital systems emerge from the interaction of technology, workflow, people, and oversight rather than from isolated algorithmic performance.[11,12] The process-deviation model fits that view because it represents safety failures as disrupted care processes, not just abnormal data points.

This framework has limitations. It is a theoretical and architectural synthesis rather than a completed empirical multidomain validation study. Some domains, particularly device safety and documentation contradiction detection, will require more heterogeneous data ingestion and natural language or multimodal extraction than current MVP domains. In addition, domain-specific severity calibration will still require local governance. Even so, the common deviation grammar remains a strong organizing principle for staged expansion.

The immediate value of this framework is translational. It provides the conceptual substrate for extending SentinelCare beyond the initial pilot domains while preserving operational consistency. That is a prerequisite for scalable patient safety intelligence.

## Conclusion

A unified domain taxonomy and process-deviation framework provides the conceptual infrastructure required for multidomain patient safety intelligence. By standardizing workflow deviation, common alert semantics, and cross-domain process measures while preserving local clinical rules, the SentinelCare model supports scalable implementation, accountable action, and comparable evaluation across heterogeneous patient safety programs.

## Funding

[Insert funding statement]

## Acknowledgments

The authors acknowledge the conceptual blueprint development and framework synthesis work that informed this manuscript.

If applicable at submission, include an AI-use disclosure consistent with journal policy.

## Conflict of Interest

[Insert conflict of interest statement]

## Data Availability

No patient-level dataset is reported in this framework paper. Non-sensitive project materials and prototype artifacts are available in the public repository: https://github.com/hssling/sentinelcare-mvp

## References

1. National Academies of Sciences, Engineering, and Medicine. Improving diagnosis in health care. Washington, DC: The National Academies Press; 2015.
2. Callen J, Georgiou A, Li J, Westbrook JI. Closing the loop on test results to reduce communication failures: a rapid review of evidence, practice and patient perspectives. BMC Health Serv Res. 2020;20:897.
3. Kwan JL, Lo L, Ferguson J, et al. Computerised clinical decision support systems and absolute improvements in care: meta-analysis of controlled clinical trials. BMJ. 2020;370:m3216.
4. Slight SP, Beeler PE, Seger DL, et al. A cross-sectional observational study of high override rates of drug allergy alerts in inpatient and outpatient settings, and opportunities for improvement. BMJ Qual Saf. 2017;26(3):217-225.
5. Nanji KC, Seger DL, Slight SP, et al. Medication-related clinical decision support alert overrides in inpatients. J Am Med Inform Assoc. 2018;25(5):476-481.
6. Evans L, Rhodes A, Alhazzani W, et al. Surviving sepsis campaign: international guidelines for management of sepsis and septic shock 2021. Crit Care Med. 2021;49(11):e1063-e1143.
7. Choi JH, Kim J, Kim J, et al. Real-time machine learning-assisted sepsis alert enhances the timeliness of antibiotic administration and diagnostic accuracy in emergency department patients with sepsis: a cluster-randomized trial. npj Digit Med. 2024;7:52.
8. World Health Organization. Global patient safety action plan 2021-2030: towards eliminating avoidable harm in health care. Geneva, Switzerland: World Health Organization; 2021.
9. World Health Organization. Global patient safety report 2024. Geneva, Switzerland: World Health Organization; 2024.
10. Institute for Healthcare Improvement. Safer together: a national action plan to advance patient safety. Boston, MA: IHI; 2022.
11. Sittig DF, Singh H. A new sociotechnical model for studying health information technology in complex adaptive healthcare systems. Qual Saf Health Care. 2010;19 Suppl 3:i68-i74.
12. Singh H, Sittig DF. A sociotechnical framework for safety-related electronic health record research reporting: the SAFER reporting framework. Ann Intern Med. 2020;172(11 Suppl):S92-S100.
