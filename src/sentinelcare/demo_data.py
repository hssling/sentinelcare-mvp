from __future__ import annotations

from datetime import timedelta

from .contracts import Event, utcnow


def demo_events() -> list[Event]:
    now = utcnow()
    return [
        Event(
            event_id="evt-med-1",
            encounter_id="enc-1001",
            patient_id="pat-501",
            event_type="order_created",
            event_time=now - timedelta(minutes=5),
            payload={
                "medication_code": "AMOX-500",
                "allergy_conflict": True,
                "renal_adjustment_required": True,
                "dose_adjusted": False,
                "egfr": 22,
            },
        ),
        Event(
            event_id="evt-lab-1",
            encounter_id="enc-1001",
            patient_id="pat-501",
            event_type="lab_reported",
            event_time=now - timedelta(minutes=40),
            payload={
                "result_code": "K+",
                "critical_flag": True,
                "acknowledged_at": None,
                "minutes_since_reported": 40,
            },
        ),
        Event(
            event_id="evt-vitals-1",
            encounter_id="enc-1001",
            patient_id="pat-501",
            event_type="vital_sign_observed",
            event_time=now,
            payload={
                "risk_score": 0.88,
                "ews_score": 8,
                "sepsis_bundle_due": True,
                "sepsis_bundle_completed": False,
                "escalation_delayed_minutes": 17,
            },
        ),
    ]


def medication_demo_events() -> list[Event]:
    now = utcnow()
    return [
        Event(
            event_id="evt-med-2",
            encounter_id="enc-2001",
            patient_id="pat-601",
            event_type="order_modified",
            event_time=now - timedelta(minutes=3),
            payload={
                "medication_code": "VANC-1G",
                "renal_adjustment_required": True,
                "dose_adjusted": False,
                "egfr": 18,
                "duplicate_therapy": True,
                "drug_class": "glycopeptide",
            },
        ),
        Event(
            event_id="evt-med-3",
            encounter_id="enc-2002",
            patient_id="pat-602",
            event_type="discharge_completed",
            event_time=now - timedelta(minutes=1),
            payload={
                "high_risk_med_omitted": True,
            },
        ),
    ]


def critical_result_demo_events() -> list[Event]:
    now = utcnow()
    return [
        Event(
            event_id="evt-lab-2",
            encounter_id="enc-3001",
            patient_id="pat-701",
            event_type="lab_reported",
            event_time=now - timedelta(minutes=62),
            payload={
                "result_code": "Lactate",
                "critical_flag": True,
                "acknowledged_at": None,
                "minutes_since_reported": 62,
            },
        ),
        Event(
            event_id="evt-lab-3",
            encounter_id="enc-3001",
            patient_id="pat-701",
            event_type="result_acknowledged",
            event_time=now - timedelta(minutes=22),
            payload={
                "documented_action": False,
            },
        ),
        Event(
            event_id="evt-lab-4",
            encounter_id="enc-3002",
            patient_id="pat-702",
            event_type="discharge_completed",
            event_time=now - timedelta(minutes=10),
            payload={
                "pending_critical_results": True,
            },
        ),
    ]


def deterioration_demo_events() -> list[Event]:
    now = utcnow()
    return [
        Event(
            event_id="evt-vitals-2",
            encounter_id="enc-4001",
            patient_id="pat-801",
            event_type="vital_sign_observed",
            event_time=now - timedelta(minutes=2),
            payload={
                "risk_score": 0.91,
                "ews_score": 9,
                "sepsis_bundle_due": True,
                "sepsis_bundle_completed": False,
                "escalation_delayed_minutes": 25,
            },
        ),
        Event(
            event_id="evt-vitals-3",
            encounter_id="enc-4002",
            patient_id="pat-802",
            event_type="vital_sign_observed",
            event_time=now - timedelta(minutes=4),
            payload={
                "risk_score": 0.55,
                "ews_score": 3,
                "sepsis_bundle_due": False,
                "sepsis_bundle_completed": False,
                "escalation_delayed_minutes": 0,
            },
        ),
    ]


def capability_demo_events() -> list[Event]:
    return (
        demo_events()
        + medication_demo_events()
        + critical_result_demo_events()
        + deterioration_demo_events()
    )
