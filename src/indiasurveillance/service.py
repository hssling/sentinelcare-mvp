from __future__ import annotations

from datetime import date
from uuid import uuid4

from .contracts import (
    ClosureRequest,
    DailySubmissionCreate,
    DailySurveillanceSubmission,
    DashboardAlert,
    DashboardIndicator,
    DashboardSnapshot,
    Department,
    EventReport,
    EventTrace,
    Facility,
    FacilityImportRecord,
    IntegrationProfile,
    LoginRequest,
    PilotStateCell,
    RegistryImportRequest,
    SessionToken,
    SubmissionReviewRequest,
    SurveillanceSnapshot,
    TraceStep,
    TriageRequest,
    UserIdentity,
)
from .demo_data import (
    build_demo_daily_submissions,
    build_demo_departments,
    build_demo_snapshot,
    build_demo_state_cells,
    build_demo_users,
)


class IndiaSurveillanceService:
    def __init__(self) -> None:
        self.snapshot = build_demo_snapshot()
        self.users = {user.user_id: user for user in build_demo_users()}
        self.users_by_username = {user.username: user for user in self.users.values() if user.username}
        self.state_cells = {cell.state_cell_id: cell for cell in build_demo_state_cells()}
        self.departments = {item.department_id: item for item in build_demo_departments()}
        self.daily_submissions = {item.submission_id: item for item in build_demo_daily_submissions()}
        self.passwords = {
            "ka-fso": "pass123",
            "tmk-ed": "pass123",
            "tmk-icu": "pass123",
            "state-ka": "pass123",
            "state-rj": "pass123",
            "national": "pass123",
            "admin": "pass123",
        }
        self.sessions: dict[str, str] = {}

    def login(self, request: LoginRequest) -> SessionToken:
        user = self.users_by_username.get(request.username)
        if user is None or self.passwords.get(request.username) != request.password:
            raise PermissionError("Invalid username or password")
        token = f"session-{uuid4()}"
        self.sessions[token] = user.user_id
        return SessionToken(access_token=token, user=user)

    def resolve_session(self, token: str | None) -> UserIdentity:
        if not token:
            raise PermissionError("Missing session token")
        user_id = self.sessions.get(token)
        if user_id is None:
            raise PermissionError("Invalid session token")
        return self.get_user(user_id)

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

    def list_departments(self, facility_id: str | None = None) -> list[Department]:
        items = list(self.departments.values())
        if facility_id:
            items = [item for item in items if item.facility_id == facility_id]
        return items

    def list_daily_submissions(self, user: UserIdentity) -> list[DailySurveillanceSubmission]:
        submissions = list(self.daily_submissions.values())
        if user.role == "facility_reporter":
            return [item for item in submissions if item.department_id == user.department_id]
        if user.role == "facility_safety_officer":
            return [item for item in submissions if item.facility_id == user.facility_id]
        if user.role == "state_cell_analyst":
            facility_ids = {item.facility_id for item in self.snapshot.facilities if item.state == user.state}
            return [item for item in submissions if item.facility_id in facility_ids]
        return submissions

    def create_daily_submission(self, request: DailySubmissionCreate, user: UserIdentity) -> DailySurveillanceSubmission:
        if user.role not in {"facility_reporter", "facility_safety_officer"}:
            raise PermissionError("User is not allowed to submit daily surveillance data")
        department = self.departments.get(request.department_id)
        if department is None:
            raise KeyError(request.department_id)
        if user.facility_id and department.facility_id != user.facility_id:
            raise PermissionError("Department does not belong to the user's facility")
        submission = DailySurveillanceSubmission(
            submission_id=f"SUB-{uuid4().hex[:8].upper()}",
            facility_id=department.facility_id,
            submitted_by=user.user_id,
            **request.model_dump(),
        )
        self.daily_submissions[submission.submission_id] = submission
        return submission

    def review_submission(self, submission_id: str, request: SubmissionReviewRequest, user: UserIdentity) -> DailySurveillanceSubmission:
        if user.role not in {"facility_safety_officer", "state_cell_analyst", "national_analyst"}:
            raise PermissionError("User is not allowed to review submissions")
        submission = self.daily_submissions.get(submission_id)
        if submission is None:
            raise KeyError(submission_id)
        submission.review_status = request.review_status
        submission.reviewed_by = request.reviewed_by
        if request.notes:
            submission.notes = f"{submission.notes} | review: {request.notes}".strip(" |")
        return submission

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

    def get_dashboard(self, user: UserIdentity) -> DashboardSnapshot:
        submissions = self.list_daily_submissions(user)
        reports = self._reports_for_user_scope(user)
        alerts = []
        if any(item.escalation_required for item in submissions):
            alerts.append(
                DashboardAlert(
                    alert_id="ALERT-ESC-001",
                    severity="severe",
                    title="Escalation required in daily surveillance feed",
                    detail="At least one department submission has escalation_required=true.",
                    owner_role="Facility safety officer" if user.role.startswith("facility") else "State cell analyst",
                )
            )
        if any(item.severe_events > 0 for item in submissions):
            alerts.append(
                DashboardAlert(
                    alert_id="ALERT-SEV-001",
                    severity="moderate",
                    title="Severe event recorded in daily submission",
                    detail="Daily surveillance data contains at least one severe event requiring review.",
                    owner_role="State cell analyst",
                )
            )
        return DashboardSnapshot(
            scope=user.role,
            indicators=[
                DashboardIndicator(label="Daily submissions", value=len(submissions), trend="stable"),
                DashboardIndicator(label="Pending review", value=len([s for s in submissions if s.review_status == "submitted"]), trend="watch"),
                DashboardIndicator(label="Open reports", value=len([r for r in reports if r.status != "closed"]), trend="watch"),
                DashboardIndicator(label="Severe daily events", value=sum(s.severe_events for s in submissions), trend="up"),
            ],
            alerts=alerts,
            submissions_pending_review=len([s for s in submissions if s.review_status == "submitted"]),
            reports_open=len([r for r in reports if r.status != "closed"]),
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

    def _reports_for_user_scope(self, user: UserIdentity) -> list[EventReport]:
        reports = self.snapshot.reports
        if user.role == "facility_reporter":
            return [item for item in reports if item.facility_id == user.facility_id]
        if user.role == "facility_safety_officer":
            return [item for item in reports if item.facility_id == user.facility_id]
        if user.role == "state_cell_analyst":
            facility_ids = {item.facility_id for item in self.snapshot.facilities if item.state == user.state}
            return [item for item in reports if item.facility_id in facility_ids]
        return reports
