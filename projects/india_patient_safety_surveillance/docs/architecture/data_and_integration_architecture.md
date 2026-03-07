# Data and Integration Architecture

## Data domains

1. facility profile and licensing metadata,
2. event reports,
3. patient/context metadata,
4. process-of-care metadata,
5. harm severity and outcome fields,
6. investigation findings,
7. corrective and preventive actions,
8. signal clusters and escalations,
9. governance and review records.

## Minimum case record

1. report identifier,
2. reporting source,
3. state, district, facility, unit,
4. event date and report date,
5. event domain,
6. process stage,
7. error type or safety deviation,
8. actual harm and potential harm,
9. narrative summary,
10. immediate action taken,
11. investigation status,
12. closure status.

## Interoperability targets

1. ABDM health facility and professional registries,
2. hospital HIS/EMR event feeds,
3. LIS/RIS critical result systems,
4. PM-JAY and payer claims review pipelines,
5. pharmacovigilance and device vigilance programs,
6. public-health surveillance platforms where patient safety overlaps with outbreak, device, blood, or medicine risk.

## Standards strategy

1. use FHIR resources where mature mappings exist,
2. allow CSV and spreadsheet templates for low-digital settings,
3. support manual forms for sentinel pilots,
4. maintain a canonical national case schema independent of source format.

## Privacy model

1. minimum necessary identifiers,
2. de-identification for higher-tier review unless case escalation requires re-identification,
3. role-based access and audit trail,
4. separate analytic extracts from operational case records.
