from __future__ import annotations

from .contracts import EventTrace, IntegrationProfile, SurveillanceSnapshot, TraceStep
from .demo_data import build_demo_snapshot


class IndiaSurveillanceService:
    def __init__(self) -> None:
        self.snapshot = build_demo_snapshot()

    def get_snapshot(self) -> SurveillanceSnapshot:
        return self.snapshot

    def get_trace(self, report_id: str) -> EventTrace:
        report = next((item for item in self.snapshot.reports if item.report_id == report_id), None)
        if report is None:
            raise KeyError(report_id)
        facility = next(item for item in self.snapshot.facilities if item.facility_id == report.facility_id)
        return EventTrace(
            report_id=report.report_id,
            facility=facility.name,
            state=facility.state,
            district=facility.district,
            domain=report.domain,
            deviation_class=report.deviation_class,
            severity=report.severity,
            validation_phase="controlled_pilot",
            active_policy_version="National minimum dataset v1 / signal rules pilot set",
            trace_steps=[
                TraceStep(step="input", finding=report.summary, output="Structured facility event record accepted."),
                TraceStep(step="taxonomy", finding=f"Mapped to domain={report.domain}, deviation={report.deviation_class}", output="Comparable surveillance classification created."),
                TraceStep(step="triage", finding=f"Severity classified as {report.severity}", output="Escalation and investigation rules selected."),
                TraceStep(step="signal", finding="Cluster and temporal rules checked against facility and state history.", output="Signal routing decision generated."),
                TraceStep(step="governance", finding="Active policy set and reporting timeline logged.", output="Audit-ready case trace stored."),
            ],
            routed_to="Facility safety officer -> district reviewer -> state cell if threshold crossed",
            closure_requirement="Investigation complete, CAPA logged, and recurrence review scheduled.",
        )

    def get_integration_profile(self) -> IntegrationProfile:
        return IntegrationProfile(
            target_systems=[
                "ABDM Health Facility Registry",
                "ABDM professional and facility registries",
                "Hospital HIS/EMR",
                "LIS/RIS and critical result systems",
                "Claims and payer review systems",
                "PvPI and haemovigilance interfaces",
                "IHIP-inspired surveillance operations layer",
            ],
            input_modes=["web form", "CSV upload", "FHIR API", "HL7 feed", "manual state batch submission"],
            standards=["FHIR", "HL7 v2", "CSV templates", "canonical surveillance JSON schema"],
            privacy_controls=[
                "role-based access control",
                "de-identification above facility tier",
                "audit trail",
                "minimum necessary identifiers",
            ],
        )
