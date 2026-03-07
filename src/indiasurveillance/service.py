from __future__ import annotations

from datetime import date

from .contracts import (
    ClosureRequest,
    EventReport,
    EventTrace,
    Facility,
    FacilityImportRecord,
    IntegrationProfile,
    PilotStateCell,
    RegistryImportRequest,
    SurveillanceSnapshot,
    TraceStep,
    TriageRequest,
    UserIdentity,
)
from .demo_data import build_demo_snapshot, build_demo_state_cells, build_demo_users


class IndiaSurveillanceService:
    def __init__(self) -> None:
        self.snapshot = build_demo_snapshot()
        self.users = {user.user_id: user for user in build_demo_users()}
        self.state_cells = {cell.state_cell_id: cell for cell in build_demo_state_cells()}

    def get_snapshot(self) -> SurveillanceSnapshot:
        return self.snapshot

    def list_users(self) -> list[UserIdentity]:
        return list(self.users.values())

    def get_user(self, user_id: str) -> UserIdentity:
        user = self.users.get(user_id)
        if user is None:
            raise KeyError(user_id)
        return user

    def list_state_cells(self) -> list[PilotStateCell]:
        return list(self.state_cells.values())

    def import_facilities(self, request: RegistryImportRequest) -> list[Facility]:
        imported = []
        for record in request.facilities:
            facility = Facility(**record.model_dump())
            existing = next((item for item in self.snapshot.facilities if item.facility_id == facility.facility_id), None)
            if existing is None:
                self.snapshot.facilities.append(facility)
                imported.append(facility)
            else:
                existing.name = facility.name
                existing.state = facility.state
                existing.district = facility.district
                existing.ownership = facility.ownership
                existing.level = facility.level
                existing.abdm_registry_ready = facility.abdm_registry_ready
                existing.registry_source = facility.registry_source
                imported.append(existing)
        self.snapshot.overview.facilities_onboarded = len(self.snapshot.facilities)
        return imported

    def triage_report(self, report_id: str, request: TriageRequest, user: UserIdentity) -> EventReport:
        report = self._get_report(report_id)
        if user.role not in {"facility_safety_officer", "state_cell_analyst", "national_analyst"}:
            raise PermissionError("User is not allowed to triage reports")
        report.status = request.status
        report.assigned_to = request.assigned_to
        report.state_cell = request.state_cell
        return report

    def close_report(self, report_id: str, request: ClosureRequest, user: UserIdentity) -> EventReport:
        report = self._get_report(report_id)
        if user.role not in {"facility_safety_officer", "state_cell_analyst", "national_analyst"}:
            raise PermissionError("User is not allowed to close reports")
        report.status = "closed"
        report.closure_note = request.closure_note
        self.snapshot.overview.open_investigations = max(self.snapshot.overview.open_investigations - 1, 0)
        return report

    def get_trace(self, report_id: str) -> EventTrace:
        report = self._get_report(report_id)
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
                TraceStep(
                    step="taxonomy",
                    finding=f"Mapped to domain={report.domain}, deviation={report.deviation_class}",
                    output="Comparable surveillance classification created.",
                ),
                TraceStep(
                    step="triage",
                    finding=f"Severity classified as {report.severity}; status={report.status}",
                    output="Escalation and investigation rules selected.",
                ),
                TraceStep(
                    step="signal",
                    finding="Cluster and temporal rules checked against facility and state history.",
                    output="Signal routing decision generated.",
                ),
                TraceStep(
                    step="governance",
                    finding="Active policy set, reporting timeline, and review owner logged.",
                    output="Audit-ready case trace stored.",
                ),
            ],
            routed_to=report.assigned_to or "Facility safety officer -> district reviewer -> state cell if threshold crossed",
            closure_requirement=report.closure_note or "Investigation complete, CAPA logged, and recurrence review scheduled.",
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

    def seed_pilot_state(self, state_name: str, facilities: list[FacilityImportRecord]) -> dict[str, object]:
        imported = self.import_facilities(RegistryImportRequest(imported_by="system", facilities=facilities))
        return {
            "state": state_name,
            "imported_facility_count": len(imported),
            "timestamp": date(2026, 3, 8).isoformat(),
        }

    def _get_report(self, report_id: str) -> EventReport:
        report = next((item for item in self.snapshot.reports if item.report_id == report_id), None)
        if report is None:
            raise KeyError(report_id)
        return report
