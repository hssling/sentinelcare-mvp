# National Minimum Dataset

## Position

The current app-level daily submission form is adequate for pilot monitoring, but it is not sufficient as the national minimum dataset for a medical error and patient safety surveillance program.

The surveillance system should operate with two linked data layers:

1. `Daily operational surveillance dataset`
2. `Event-level investigation dataset`

The first supports burden monitoring and escalation screening. The second supports causal analysis, policy learning, prevention, and AI-assisted surveillance.

## Dataset structure

### A. Facility and reporting context

Required fields:

1. `report_id`
2. `source_mode`
   - manual_daily_submission
   - manual_event_report
   - sentinelcare_detected_event
   - batch_import
   - API_feed
3. `reporting_timestamp`
4. `event_timestamp`
5. `state`
6. `district`
7. `facility_id`
8. `facility_name`
9. `department_id`
10. `department_name`
11. `unit_or_ward`
12. `encounter_setting`
    - emergency
    - outpatient
    - inpatient
    - ICU
    - operation_theatre
    - labour_room
    - day_care
13. `shift`
    - morning
    - evening
    - night
14. `reporter_role`
15. `review_owner_role`

### B. Patient and case context

Required minimum:

1. `patient_age_band`
2. `patient_sex`
3. `special_population_flag`
   - neonatal
   - pediatric
   - obstetric
   - geriatric
   - critical_care
4. `encounter_id_local`
5. `admission_date`
6. `discharge_status`
7. `primary_service`
8. `high_risk_flag`

For higher tiers, identifiers should be de-identified unless escalation requires re-identification.

### C. Safety event classification

Required:

1. `domain`
   - medication
   - diagnostic
   - procedure
   - deterioration
   - infection_environment
   - lab_radiology
   - care_transition
   - documentation_communication
   - device_equipment
   - operational
2. `deviation_class`
   - omission
   - contradiction
   - harmful_delay
   - sequencing_mismatch
   - closure_failure
3. `process_stage`
4. `event_type`
5. `actual_harm`
6. `potential_harm`
7. `severity_level`
8. `preventability_rating`
9. `detectability_rating`
10. `recurrence_flag`

### D. Narrative and evidence

Required:

1. `event_summary`
2. `what_was_expected`
3. `what_happened`
4. `immediate_action_taken`
5. `evidence_source`
   - manual narrative
   - chart review
   - vital sign stream
   - lab result
   - pharmacy order
   - imaging result
   - claims/audit
6. `linked_system_trace_id`
7. `linked_policy_version`

### E. Contributing factors

Required coded multi-select:

1. `staffing_workload`
2. `handover_communication`
3. `documentation_quality`
4. `protocol_nonadherence`
5. `equipment_issue`
6. `drug_stockout_or_supply_issue`
7. `diagnostic_delay`
8. `referral_delay`
9. `digital_system_issue`
10. `human_factor_cognitive`
11. `training_or_supervision_gap`
12. `environmental_or_infrastructure_issue`

### F. Investigation and CAPA

Required:

1. `triage_status`
2. `investigation_status`
3. `investigation_method`
   - desk review
   - mini RCA
   - full RCA
   - mortality review
   - safety huddle review
4. `root_cause_category`
5. `corrective_action`
6. `preventive_action`
7. `owner_assigned`
8. `due_date`
9. `closure_status`
10. `closure_date`
11. `closure_quality_rating`

### G. Denominator and activity data

Required by department and facility per reporting day:

1. `patient_days`
2. `admissions`
3. `discharges`
4. `ED_visits`
5. `ICU_patient_days`
6. `surgeries`
7. `deliveries`
8. `medication_orders`
9. `critical_results_count`
10. `device_days`
11. `central_line_days`
12. `ventilator_days`
13. `urinary_catheter_days`

### H. Operational context

Strongly recommended:

1. `bed_occupancy_rate`
2. `staffing_shortfall_flag`
3. `system_downtime_flag`
4. `lab_turnaround_breach_flag`
5. `radiology_turnaround_breach_flag`
6. `stockout_flag`
7. `crowding_flag`

## Dataset tiers

### Tier 1: Minimum pilot dataset

Use when digitization is low:

1. daily counts
2. event domain
3. severity
4. process stage
5. summary
6. immediate action
7. review status

### Tier 2: Operational surveillance dataset

Use for state pilots:

1. all Tier 1 fields
2. patient context
3. contributing factors
4. denominator fields
5. audit and trace linkage

### Tier 3: Learning health system dataset

Use when integrating with SentinelCare and hospital systems:

1. machine-detected event stream
2. temporal features
3. system traces
4. AI-assist outputs
5. CAPA outcome tracking

## Assessment of current app

Current app status:

1. adequate for Tier 1 daily burden monitoring
2. partially adequate for Tier 2 workflow tracking
3. not yet adequate for national learning, causal analysis, or AI-enabled prevention

Therefore the current data collection is useful, but not comprehensive enough on its own.
