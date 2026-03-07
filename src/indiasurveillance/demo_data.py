from __future__ import annotations

from datetime import date, datetime, timedelta

from .contracts import EventReport, Facility, PolicyRecord, SafetySignal, SurveillanceSnapshot


def build_demo_snapshot() -> SurveillanceSnapshot:
    now = datetime(2026, 3, 7, 18, 0, 0)
    facilities = [
        Facility(
            facility_id="FAC-TMK-001",
            name="Shridevi Institute of Medical Sciences and Research Hospital",
            state="Karnataka",
            district="Tumkur",
            ownership="teaching",
            level="medical_college",
            abdm_registry_ready=True,
        ),
        Facility(
            facility_id="FAC-DLH-014",
            name="District Hospital Jaipur Sentinel Site",
            state="Rajasthan",
            district="Jaipur",
            ownership="public",
            level="district_hospital",
            abdm_registry_ready=True,
        ),
        Facility(
            facility_id="FAC-KOL-022",
            name="Metro Multispeciality Safety Network Site",
            state="West Bengal",
            district="Kolkata",
            ownership="private",
            level="private_hospital",
            abdm_registry_ready=False,
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
