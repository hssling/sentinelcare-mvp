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

