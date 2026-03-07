from __future__ import annotations

from .contracts import Alert, Severity


class AlertRouter:
    def route(self, alert: Alert) -> Alert:
        recipients = ["duty_doctor"]

        if alert.domain == "medication_safety":
            recipients.append("pharmacist")
        if alert.domain == "critical_result_closure":
            recipients.append("lab_team")
        if alert.domain == "deterioration_surveillance":
            recipients.append("bedside_nurse")

        if alert.severity in {Severity.URGENT_ESCALATION, Severity.HARD_STOP_PROPOSAL}:
            recipients.append("consultant")
            recipients.append("safety_officer")

        alert.routed_to = sorted(set(recipients))
        return alert

