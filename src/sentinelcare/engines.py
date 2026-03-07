from __future__ import annotations

from uuid import uuid4

from .contracts import Alert, Event, Severity, utcnow


class MedicationSafetyEngine:
    domain = "medication_safety"

    def run(self, event: Event) -> list[Alert]:
        if event.event_type not in {"order_created", "order_modified", "discharge_completed"}:
            return []

        payload = event.payload
        alerts: list[Alert] = []

        if payload.get("allergy_conflict") is True:
            alerts.append(
                self._mk_alert(
                    event,
                    "hard_contraindication",
                    Severity.HARD_STOP_PROPOSAL,
                    0.98,
                    {"reason": "allergy_conflict", "medication": payload.get("medication_code")},
                    {"action": "block_order_and_page_pharmacist"},
                )
            )

        if payload.get("renal_adjustment_required") is True and payload.get("dose_adjusted") is False:
            alerts.append(
                self._mk_alert(
                    event,
                    "dose_adjustment_warning",
                    Severity.WARNING,
                    0.86,
                    {"reason": "renal_adjustment_missing", "egfr": payload.get("egfr")},
                    {"action": "review_and_adjust_dose"},
                )
            )

        if payload.get("duplicate_therapy") is True:
            alerts.append(
                self._mk_alert(
                    event,
                    "duplicate_therapy_flag",
                    Severity.PRECAUTION,
                    0.82,
                    {"reason": "duplicate_therapy", "drug_class": payload.get("drug_class")},
                    {"action": "reconcile_active_medications"},
                )
            )

        if event.event_type == "discharge_completed" and payload.get("high_risk_med_omitted") is True:
            alerts.append(
                self._mk_alert(
                    event,
                    "omitted_high_risk_med_suggestion",
                    Severity.RECOMMENDATION,
                    0.77,
                    {"reason": "high_risk_med_omitted"},
                    {"action": "discharge_med_reconciliation"},
                )
            )

        return alerts

    def _mk_alert(
        self,
        event: Event,
        alert_type: str,
        severity: Severity,
        confidence: float,
        evidence: dict,
        action: dict,
    ) -> Alert:
        return Alert(
            alert_id=str(uuid4()),
            encounter_id=event.encounter_id,
            patient_id=event.patient_id,
            generated_at=utcnow(),
            domain=self.domain,
            alert_type=alert_type,
            severity=severity,
            confidence_score=confidence,
            evidence=evidence,
            recommended_action=action,
        )


class CriticalResultClosureEngine:
    domain = "critical_result_closure"

    def run(self, event: Event) -> list[Alert]:
        payload = event.payload
        alerts: list[Alert] = []

        if event.event_type == "lab_reported":
            is_critical = payload.get("critical_flag") is True
            acknowledged = payload.get("acknowledged_at") is not None
            age_minutes = float(payload.get("minutes_since_reported", 0))
            if is_critical and not acknowledged and age_minutes >= 30:
                alerts.append(
                    self._mk_alert(
                        event,
                        "critical_result_unacknowledged",
                        Severity.URGENT_ESCALATION,
                        0.93,
                        {"result_code": payload.get("result_code"), "minutes_since_reported": age_minutes},
                        {"action": "escalate_to_responsible_team"},
                    )
                )

        if event.event_type == "discharge_completed" and payload.get("pending_critical_results") is True:
            alerts.append(
                self._mk_alert(
                    event,
                    "pending_result_after_discharge",
                    Severity.WARNING,
                    0.88,
                    {"reason": "critical_results_pending_after_discharge"},
                    {"action": "create_follow_up_task_and_assign_owner"},
                )
            )

        if event.event_type == "result_acknowledged" and payload.get("documented_action") is False:
            alerts.append(
                self._mk_alert(
                    event,
                    "no_documented_action",
                    Severity.PRECAUTION,
                    0.79,
                    {"reason": "acknowledged_without_documented_action"},
                    {"action": "request_action_documentation"},
                )
            )

        return alerts

    def _mk_alert(
        self,
        event: Event,
        alert_type: str,
        severity: Severity,
        confidence: float,
        evidence: dict,
        action: dict,
    ) -> Alert:
        return Alert(
            alert_id=str(uuid4()),
            encounter_id=event.encounter_id,
            patient_id=event.patient_id,
            generated_at=utcnow(),
            domain=self.domain,
            alert_type=alert_type,
            severity=severity,
            confidence_score=confidence,
            evidence=evidence,
            recommended_action=action,
        )


class DeteriorationSurveillanceEngine:
    domain = "deterioration_surveillance"

    def run(self, event: Event) -> list[Alert]:
        if event.event_type not in {"vital_sign_observed", "escalation_triggered"}:
            return []

        payload = event.payload
        alerts: list[Alert] = []

        risk_score = float(payload.get("risk_score", 0.0))
        ews = float(payload.get("ews_score", 0.0))
        sepsis_bundle_due = payload.get("sepsis_bundle_due") is True
        sepsis_bundle_completed = payload.get("sepsis_bundle_completed") is True
        escalation_delayed = payload.get("escalation_delayed_minutes", 0) >= 15

        if risk_score >= 0.8 or ews >= 7:
            alerts.append(
                self._mk_alert(
                    event,
                    "rising_risk_watchlist",
                    Severity.WARNING,
                    0.87,
                    {"risk_score": risk_score, "ews_score": ews},
                    {"action": "nurse_doctor_action_prompt"},
                )
            )

        if sepsis_bundle_due and not sepsis_bundle_completed:
            alerts.append(
                self._mk_alert(
                    event,
                    "sepsis_bundle_deviation",
                    Severity.URGENT_ESCALATION,
                    0.91,
                    {"sepsis_bundle_due": True, "completed": False},
                    {"action": "launch_sepsis_checklist_and_notify_team"},
                )
            )

        if escalation_delayed:
            alerts.append(
                self._mk_alert(
                    event,
                    "delayed_escalation",
                    Severity.URGENT_ESCALATION,
                    0.83,
                    {"delay_minutes": payload.get("escalation_delayed_minutes")},
                    {"action": "escalate_to_senior_clinician"},
                )
            )

        return alerts

    def _mk_alert(
        self,
        event: Event,
        alert_type: str,
        severity: Severity,
        confidence: float,
        evidence: dict,
        action: dict,
    ) -> Alert:
        return Alert(
            alert_id=str(uuid4()),
            encounter_id=event.encounter_id,
            patient_id=event.patient_id,
            generated_at=utcnow(),
            domain=self.domain,
            alert_type=alert_type,
            severity=severity,
            confidence_score=confidence,
            evidence=evidence,
            recommended_action=action,
        )

