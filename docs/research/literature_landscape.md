# Literature Landscape for SentinelCare

## Purpose

This document summarizes core evidence and policy sources used to ground SentinelCare's design and publication strategy.

## Core policy and safety frameworks

1. WHO Global Patient Safety Action Plan 2021-2030  
Source: https://www.who.int/publications/i/item/9789240032705  
Relevance: establishes systems-level patient safety priorities, including digital safety infrastructure and learning systems.

2. WHO Global Patient Safety Report 2024  
Source: https://iris.who.int/handle/10665/376928  
Relevance: global baseline for implementation maturity and system gaps.

3. National Action Plan to Advance Patient Safety (IHI/National Steering Committee)  
Source: https://www.ihi.org/national-action-plan-advance-patient-safety  
Relevance: U.S.-oriented systems strategy across governance, culture, and learning.

4. National Academies report: Improving Diagnosis in Health Care (2015)  
Source: https://www.nationalacademies.org/publications/21794  
Relevance: diagnostic errors as a major preventable harm category and rationale for closed-loop diagnostic follow-up.

## Regulatory and trustworthy AI guidance

1. FDA Clinical Decision Support Software Guidance (revised Jan 2026)  
Source: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software  
Relevance: defines non-device/device CDS boundaries and transparency expectations.

2. FDA Good Machine Learning Practice (GMLP) Guiding Principles  
Source: https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles  
Relevance: lifecycle quality controls for ML-enabled clinical software.

3. ONC Decision Support Interventions (DSI) transparency criteria  
Source: https://www.healthit.gov/test-method/decision-support-interventions  
Relevance: source attribute disclosure and explainability alignment for U.S. certified health IT.

## Clinical domain guidelines aligned to MVP scope

1. Sepsis management: Surviving Sepsis Campaign 2021  
Source: https://pubmed.ncbi.nlm.nih.gov/34599691/  
Relevance: supports deterioration/sepsis surveillance and timely intervention workflow.

2. Test result communication and critical values (Joint Commission references/FAQ)  
Source: https://www.jointcommission.org/standards/standard-faqs/critical-access-hospital/national-patient-safety-goals-npsg/000001556  
Relevance: supports critical result closure workflow and escalation accountability.

3. Medication safety with CPOE/CDS systematic reviews  
Sources:  
- https://pubmed.ncbi.nlm.nih.gov/30463867/  
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2359507/  
Relevance: supports medication safety engine strategy and highlights alert fatigue tradeoffs.

## Existing systems and implementation evidence

1. Epic Sepsis Model external validation (JAMA Internal Medicine)  
Source: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307  
Relevance: demonstrates performance variability and need for local validation/governance.

2. Epic model external validation in county EDs (JAMIA Open 2024)  
Source: https://pubmed.ncbi.nlm.nih.gov/39545248/  
Relevance: confirms context sensitivity in real-world deployments.

3. Real-time ML-assisted sepsis alert cluster-randomized trial  
Source: https://pubmed.ncbi.nlm.nih.gov/38381351/  
Relevance: evidence that real-time alerting can improve timeliness under operational constraints.

4. Closing the loop on test result communication rapid review  
Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC7510293/  
Relevance: supports design emphasis on closed-loop communication.

## Key evidence-to-design implications

1. Precision and alert burden must be co-optimized, not treated independently.
2. Closed-loop ownership and acknowledgment are required to reduce follow-up failures.
3. Site adaptation is necessary because transportability is limited across settings.
4. Explainability and source-attribution are now both safety and regulatory requirements.
5. Human-in-the-loop escalation pathways are mandatory for high-risk outputs.

