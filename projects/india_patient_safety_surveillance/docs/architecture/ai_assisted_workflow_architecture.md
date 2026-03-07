# AI-Assisted Workflow Architecture

## Position

AI should be integrated into the workflow, but only as a bounded assistance layer.

It should improve:

1. detection,
2. triage,
3. clustering,
4. summarization,
5. prevention planning,
6. surveillance interpretation.

It should not act as an autonomous clinical decision-maker or case closer.

## AI roles in the workflow

### 1. Intake assistance

Functions:

1. convert free-text descriptions into structured fields
2. suggest domain and deviation class
3. identify missing mandatory fields
4. detect likely duplicates

Outputs:

1. suggested taxonomy labels
2. missing-data prompts
3. confidence score

Human owner:

1. reporter
2. facility safety officer

### 2. Detection assistance

Functions:

1. anomaly detection on daily surveillance counts
2. cluster detection across sites and time
3. identification of hidden case relationships
4. triage priority scoring

Outputs:

1. candidate signals
2. risk score
3. cluster membership suggestions

Human owner:

1. state cell analyst
2. national analyst

### 3. Case review assistance

Functions:

1. summarize long narratives and source traces
2. extract likely contributing factors
3. suggest comparable prior cases
4. propose candidate CAPA options

Outputs:

1. review summary
2. factor shortlist
3. precedent retrieval
4. CAPA suggestions

Human owner:

1. facility safety officer
2. district reviewer
3. state analyst

### 4. Governance assistance

Functions:

1. check policy completeness
2. detect overdue closure paths
3. highlight inconsistent adjudication across sites
4. prepare state/national surveillance briefs

Outputs:

1. governance exceptions
2. closure quality warnings
3. draft bulletin text

Human owner:

1. governance administrator
2. national analyst

## Safe AI design rules

### Rule 1. Human decision ownership

AI may recommend:

1. triage priority
2. classification
3. CAPA options

AI must not finalize:

1. legal attribution
2. disciplinary action
3. case closure
4. patient care action without human owner

### Rule 2. Explainability

Every AI output should store:

1. input source
2. model or policy version
3. output label
4. confidence score
5. evidence snippet
6. final human override if applicable

### Rule 3. Validation before scale

AI deployment path:

1. retrospective validation
2. silent mode
3. controlled pilot
4. constrained production
5. monitored scale-up

### Rule 4. Auditability

All AI-assisted decisions need durable logs:

1. generated suggestion
2. who accepted or rejected it
3. what changed afterward
4. downstream outcome

## Technical AI modules

### Module A. Narrative structuring model

Input:

1. free-text event descriptions
2. review notes
3. trace summaries

Output:

1. structured event type
2. candidate severity
3. candidate contributing factors

Best suited methods:

1. LLM-assisted extraction
2. constrained schema filling

### Module B. Multi-site clustering engine

Input:

1. event-level structured records
2. manual and SentinelCare-generated cases
3. time and geography metadata

Output:

1. probable clusters
2. trend anomalies
3. cluster severity score

Best suited methods:

1. embeddings plus similarity search
2. temporal anomaly detection
3. rule overlays

### Module C. Triage prioritization model

Input:

1. severity
2. process stage
3. recurrence
4. patient context
5. contributing factors
6. cluster burden

Output:

1. review priority
2. escalation recommendation

Best suited methods:

1. interpretable gradient boosting
2. calibrated risk scoring

### Module D. CAPA retrieval assistant

Input:

1. structured case profile
2. historical closed cases
3. policy library

Output:

1. comparable past cases
2. candidate actions
3. implementation watchouts

Best suited methods:

1. retrieval-augmented generation
2. policy-grounded prompting

## AI integration points in the current workflow

### Current manual entry workflow

Insert AI at:

1. form submission quality checks
2. classification suggestion
3. escalation suggestion

### Current report queue

Insert AI at:

1. duplicate case detection
2. prioritization
3. summary generation

### Current governance dashboard

Insert AI at:

1. audit anomaly detection
2. draft state/national summaries
3. overdue closure prioritization

## How this aligns with SentinelCare

SentinelCare becomes the clinical AI and agent execution layer.

India Surveillance becomes the surveillance operations and governance layer.

The AI architecture should therefore be split:

1. `workflow AI`
   - text extraction
   - triage support
   - CAPA retrieval
2. `clinical safety AI`
   - prospective detection
   - deterioration risk
   - medication contradiction checks
   - critical-result closure failure detection

## Recommended governance controls

Each AI module should have:

1. model card
2. intended-use statement
3. excluded-use statement
4. validation report
5. drift monitoring plan
6. rollback procedure
7. human override requirement

## Recommended next build steps

### Step 1

Add AI-ready fields to the canonical dataset:

1. confidence score
2. source provenance
3. human adjudication
4. override rationale

### Step 2

Add AI assistance endpoints:

1. `/ai/classify-event`
2. `/ai/triage-score`
3. `/ai/cluster-suggestions`
4. `/ai/capa-suggestions`

### Step 3

Run in silent mode before visible production use

### Step 4

Measure:

1. sensitivity gain
2. review burden
3. false positive load
4. closure time
5. prevention impact

## Conclusion

AI should be integrated, but in a controlled, explainable, auditable, human-supervised manner.

The most valuable role is not generic automation. It is selective workflow assistance tightly connected to:

1. the national dataset,
2. the SentinelCare agent layer,
3. the review and governance chain,
4. the prevention and learning loop.
