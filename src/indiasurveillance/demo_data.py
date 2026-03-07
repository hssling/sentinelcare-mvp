from __future__ import annotations

from datetime import date, datetime, timedelta

from .contracts import (
    DailySurveillanceSubmission,
    Department,
    EventReport,
    Facility,
    PilotStateCell,
    PolicyRecord,
    SafetySignal,
    SurveillanceSnapshot,
    UserIdentity,
)


def build_demo_snapshot() -> SurveillanceSnapshot:
    now = datetime(2026, 3, 8, 9, 0, 0)
    facilities = [
        Facility(
            facility_id="FAC-TMK-001",
            name="Shridevi Institute of Medical Sciences and Research Hospital",
            state="Karnataka",
            district="Tumkur",
            ownership="teaching",
            level="medical_college",
            abdm_registry_ready=True,
            registry_source="abdm_seed",
        ),
        Facility(
            facility_id="FAC-DLH-014",
            name="District Hospital Jaipur Sentinel Site",
            state="Rajasthan",
            district="Jaipur",
            ownership="public",
            level="district_hospital",
            abdm_registry_ready=True,
            registry_source="state_registry",
        ),
        Facility(
            facility_id="FAC-KOL-022",
            name="Metro Multispeciality Safety Network Site",
            state="West Bengal",
            district="Kolkata",
            ownership="private",
            level="private_hospital",
            abdm_registry_ready=False,
            registry_source="manual",
        ),
    ]
    reports = [
        EventReport(
            report_id="EVT-IND-1001",
            event_date=date(2026, 3, 6),
            reported_at=now - timedelta(hours=20),
            facility_id="FAC-TMK-001",
            patient_context="Adult inpatient, post-operative ward",
            domain="medication",
            deviation_class="contradiction",
            severity="moderate",
            process_stage="order -> verification -> administration",
            summary="Beta-lactam order placed despite allergy documentation mismatch.",
            immediate_action="Order held and pharmacist alerted.",
            status="investigating",
            assigned_to="State clinical pharmacist reviewer",
            state_cell="Karnataka state cell",
        ),
        EventReport(
            report_id="EVT-IND-1002",
            event_date=date(2026, 3, 5),
            reported_at=now - timedelta(days=1, hours=3),
            facility_id="FAC-DLH-014",
            patient_context="Emergency department, suspected sepsis",
            domain="deterioration",
            deviation_class="harmful_delay",
            severity="severe",
            process_stage="recognition -> escalation -> treatment",
            summary="Delayed escalation after repeated abnormal vitals and lactate trigger.",
            immediate_action="Rapid response review initiated.",
            status="triaged",
            assigned_to="Rajasthan state patient safety cell",
            state_cell="Rajasthan state cell",
        ),
        EventReport(
            report_id="EVT-IND-1003",
            event_date=date(2026, 3, 4),
            reported_at=now - timedelta(days=2),
            facility_id="FAC-KOL-022",
            patient_context="Outpatient imaging follow-up",
            domain="lab_radiology",
            deviation_class="closure_failure",
            severity="moderate",
            process_stage="result -> acknowledgement -> follow-up -> closure",
            summary="Critical imaging result acknowledged but no documented clinician follow-up.",
            immediate_action="Case escalated to facility safety officer.",
            status="reported",
        ),
    ]
    signals = [
        SafetySignal(
            signal_id="SIG-KA-01",
            title="Medication allergy contradiction cluster",
            scope="facility",
            state="Karnataka",
            district="Tumkur",
            domain="medication",
            deviation_class="contradiction",
            severity="moderate",
            reports_linked=4,
            owner_role="Facility medication safety lead",
            next_action="Review allergy documentation workflow and CPOE reconciliation.",
            status="investigate",
        ),
        SafetySignal(
            signal_id="SIG-IN-02",
            title="Delayed escalation in deterioration pathways",
            scope="state",
            state="Rajasthan",
            district=None,
            domain="deterioration",
            deviation_class="harmful_delay",
            severity="severe",
            reports_linked=9,
            owner_role="State patient safety intelligence cell",
            next_action="Conduct focused review of ED escalation and sepsis bundle completion.",
            status="escalated",
        ),
    ]
    policies = [
        PolicyRecord(
            policy_id="POL-IND-001",
            title="National minimum patient safety dataset v1",
            state="approved_pilot",
            validation_phase="controlled_pilot",
            approver="National steering group",
            activation_scope="Sentinel states",
            last_updated=date(2026, 3, 1),
        ),
        PolicyRecord(
            policy_id="POL-IND-002",
            title="Sentinel event 24-hour reporting rule",
            state="approved_production",
            validation_phase="scale_up",
            approver="National steering group",
            activation_scope="National",
            last_updated=date(2026, 2, 20),
        ),
    ]
    return SurveillanceSnapshot(
        overview={
            "reporting_period": "March 2026 demo snapshot",
            "facilities_onboarded": 42,
            "states_covered": 8,
            "reports_received": 186,
            "open_investigations": 31,
            "escalated_signals": 7,
            "sentinel_events": 3,
            "validation_phase": "controlled_pilot",
        },
        facilities=facilities,
        reports=reports,
        signals=signals,
        policies=policies,
    )


def build_demo_users() -> list[UserIdentity]:
    return [
        UserIdentity(
            user_id="demo-fso-ka",
            name="Karnataka Facility Safety Officer",
            role="facility_safety_officer",
            state="Karnataka",
            district="Tumkur",
            facility_id="FAC-TMK-001",
            username="ka-fso",
        ),
        UserIdentity(
            user_id="demo-ed-ka",
            name="Tumkur Emergency Department Reporter",
            role="facility_reporter",
            state="Karnataka",
            district="Tumkur",
            facility_id="FAC-TMK-001",
            department_id="DEPT-TMK-ED",
            username="tmk-ed",
        ),
        UserIdentity(
            user_id="demo-icu-ka",
            name="Tumkur ICU Reporter",
            role="facility_reporter",
            state="Karnataka",
            district="Tumkur",
            facility_id="FAC-TMK-001",
            department_id="DEPT-TMK-ICU",
            username="tmk-icu",
        ),
        UserIdentity(
            user_id="demo-state-ka",
            name="Karnataka State Cell Analyst",
            role="state_cell_analyst",
            state="Karnataka",
            username="state-ka",
        ),
        UserIdentity(
            user_id="demo-state-rj",
            name="Rajasthan State Cell Analyst",
            role="state_cell_analyst",
            state="Rajasthan",
            username="state-rj",
        ),
        UserIdentity(
            user_id="demo-national",
            name="National Surveillance Analyst",
            role="national_analyst",
            username="national",
        ),
        UserIdentity(
            user_id="demo-admin",
            name="Governance Administrator",
            role="governance_admin",
            username="admin",
        ),
    ]


def build_demo_state_cells() -> list[PilotStateCell]:
    return [
        PilotStateCell(
            state_cell_id="STATE-KA",
            state="Karnataka",
            nodal_unit="State patient safety intelligence cell",
            lead_name="State Quality and Safety Lead",
            status="pilot",
            facilities_mapped=12,
        ),
        PilotStateCell(
            state_cell_id="STATE-RJ",
            state="Rajasthan",
            nodal_unit="State patient safety intelligence cell",
            lead_name="State Epidemiology and Quality Lead",
            status="pilot",
            facilities_mapped=9,
        ),
    ]


def build_demo_departments() -> list[Department]:
    return [
        Department(department_id="DEPT-TMK-ED", facility_id="FAC-TMK-001", name="Emergency Department", category="clinical"),
        Department(department_id="DEPT-TMK-ICU", facility_id="FAC-TMK-001", name="ICU", category="clinical"),
        Department(department_id="DEPT-TMK-OT", facility_id="FAC-TMK-001", name="Operation Theatre", category="clinical"),
        Department(department_id="DEPT-TMK-QA", facility_id="FAC-TMK-001", name="Quality Cell", category="quality"),
        Department(department_id="DEPT-JPR-ED", facility_id="FAC-DLH-014", name="Emergency Department", category="clinical"),
        Department(department_id="DEPT-KOL-RAD", facility_id="FAC-KOL-022", name="Radiology", category="support"),
    ]


def build_demo_daily_submissions() -> list[DailySurveillanceSubmission]:
    today = date(2026, 3, 8)
    now = datetime(2026, 3, 8, 9, 0, 0)
    return [
        DailySurveillanceSubmission(
            submission_id="SUB-TMK-001",
            submission_date=today,
            facility_id="FAC-TMK-001",
            department_id="DEPT-TMK-ED",
            submitted_by="demo-ed-ka",
            patient_days=118,
            near_misses=4,
            no_harm_events=2,
            harm_events=1,
            severe_events=0,
            medication_events=2,
            procedure_events=0,
            infection_events=0,
            diagnostic_events=1,
            escalation_required=False,
            notes="High near-miss load during evening shift handover.",
            created_at=now,
            updated_at=now,
        ),
        DailySurveillanceSubmission(
            submission_id="SUB-TMK-002",
            submission_date=today,
            facility_id="FAC-TMK-001",
            department_id="DEPT-TMK-ICU",
            submitted_by="demo-icu-ka",
            patient_days=36,
            near_misses=2,
            no_harm_events=1,
            harm_events=1,
            severe_events=1,
            medication_events=1,
            procedure_events=0,
            infection_events=1,
            diagnostic_events=0,
            escalation_required=True,
            notes="One deterioration escalation breach triggered review.",
            created_at=now,
            updated_at=now,
        ),
    ]
