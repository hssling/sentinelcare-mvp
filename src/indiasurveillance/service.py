from __future__ import annotations

import os
from datetime import date, datetime, timezone
from uuid import uuid4

from .contracts import (
    AuditLogRecord,
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
    NotificationAcknowledgeRequest,
    NotificationRecord,
    PilotStateCell,
    RegistryImportRequest,
    SessionToken,
    SubmissionReviewRequest,
    SurveillanceSnapshot,
    TraceStep,
    TrendSeries,
    TriageRequest,
    UserCreateRequest,
    UserIdentity,
    UserRecord,
)
from .demo_data import build_demo_snapshot
from .persistence import InMemoryStorage, StorageBackend, SupabaseStorage
from .security import decode_access_token, hash_password, issue_access_token, verify_password


class IndiaSurveillanceService:
    def __init__(self, storage: StorageBackend | None = None, jwt_secret: str | None = None) -> None:
        self.storage = storage or self._build_storage_from_env()
        self.jwt_secret = jwt_secret or os.getenv("INDIA_SURVEILLANCE_JWT_SECRET", "india-surveillance-dev-secret-2026-secure-key")
        self.storage.bootstrap_if_empty()

    def _build_storage_from_env(self) -> StorageBackend:
        url = os.getenv("SUPABASE_INDIA_URL") or os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_INDIA_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if url and key:
            return SupabaseStorage(url, key)
        return InMemoryStorage()

    def login(self, request: LoginRequest) -> SessionToken:
        user = self.storage.get_user_by_username(request.username)
        if user is None or not verify_password(request.password, user.password_hash, user.password_salt):
            raise PermissionError("Invalid username or password")
        if not user.is_active:
            raise PermissionError("User is inactive")
        token, expires_at = issue_access_token(user.user_id, self.jwt_secret)
        self._audit(user.user_id, "auth.login", "user", user.user_id, f"Login for {user.username}")
        return SessionToken(access_token=token, expires_at=expires_at, user=self._identity(user))

    def resolve_session(self, token: str | None) -> UserIdentity:
        if not token:
            raise PermissionError("Missing access token")
        user_id = decode_access_token(token, self.jwt_secret)
        user = self.storage.get_user(user_id)
        if user is None or not user.is_active:
            raise PermissionError("Invalid access token")
        return self._identity(user)

    def get_snapshot(self) -> SurveillanceSnapshot:
        overview = self._overview()
        return SurveillanceSnapshot(
            overview=overview,
            facilities=self.storage.list_facilities(),
            reports=self.storage.list_reports(),
            signals=self.storage.list_signals(),
            policies=self.storage.list_policies(),
        )

    def list_users(self, current_user: UserIdentity | None = None) -> list[UserIdentity]:
        users = [self._identity(item) for item in self.storage.list_users()]
        if current_user and current_user.role == "facility_safety_officer":
            return [item for item in users if item.facility_id == current_user.facility_id]
        if current_user and current_user.role == "state_cell_analyst":
            return [item for item in users if item.state == current_user.state]
        return users

    def create_user(self, request: UserCreateRequest, current_user: UserIdentity) -> UserIdentity:
        if current_user.role not in {"facility_safety_officer", "state_cell_analyst", "governance_admin", "national_analyst"}:
            raise PermissionError("User is not allowed to create accounts")
        if self.storage.get_user_by_username(request.username):
            raise ValueError("Username already exists")
        if current_user.role == "facility_safety_officer":
            request.facility_id = current_user.facility_id
            if request.role not in {"facility_reporter", "facility_safety_officer"}:
                raise PermissionError("Facility safety officer can only create facility-level accounts")
        if current_user.role == "state_cell_analyst":
            request.state = current_user.state
            if request.role not in {"district_reviewer", "state_cell_analyst", "facility_safety_officer", "facility_reporter"}:
                raise PermissionError("State analyst can only create state pilot accounts")
        password_hash, password_salt = hash_password(request.password)
        user = UserRecord(
            user_id=f"USR-{uuid4().hex[:10]}",
            created_at=datetime.now(timezone.utc),
            created_by=current_user.user_id,
            password_hash=password_hash,
            password_salt=password_salt,
            **request.model_dump(),
        )
        self.storage.create_user(user)
        self._audit(current_user.user_id, "user.create", "user", user.user_id, f"Created {user.username} as {user.role}")
        return self._identity(user)

    def get_user(self, user_id: str) -> UserIdentity:
        user = self.storage.get_user(user_id)
        if user is None:
            raise KeyError(user_id)
        return self._identity(user)

    def list_state_cells(self) -> list[PilotStateCell]:
        return self.storage.list_state_cells()

    def list_departments(self, user: UserIdentity, facility_id: str | None = None) -> list[Department]:
        if user.role in {"facility_reporter", "facility_safety_officer"}:
            facility_id = user.facility_id
        return self.storage.list_departments(facility_id)

    def list_daily_submissions(self, user: UserIdentity) -> list[DailySurveillanceSubmission]:
        submissions = self.storage.list_daily_submissions()
        if user.role == "facility_reporter":
            return [item for item in submissions if item.department_id == user.department_id]
        if user.role == "facility_safety_officer":
            return [item for item in submissions if item.facility_id == user.facility_id]
        if user.role == "state_cell_analyst":
            facility_ids = {item.facility_id for item in self.storage.list_facilities() if item.state == user.state}
            return [item for item in submissions if item.facility_id in facility_ids]
        return submissions

    def list_reports(self, user: UserIdentity) -> list[EventReport]:
        return self._reports_for_user_scope(user)

    def create_daily_submission(self, request: DailySubmissionCreate, user: UserIdentity) -> DailySurveillanceSubmission:
        if user.role not in {"facility_reporter", "facility_safety_officer"}:
            raise PermissionError("User is not allowed to submit daily surveillance data")
        department = next((item for item in self.storage.list_departments() if item.department_id == request.department_id), None)
        if department is None:
            raise KeyError(request.department_id)
        if user.facility_id and department.facility_id != user.facility_id:
            raise PermissionError("Department does not belong to the user's facility")
        now = datetime.now(timezone.utc)
        submission = DailySurveillanceSubmission(
            submission_id=f"SUB-{uuid4().hex[:8].upper()}",
            facility_id=department.facility_id,
            submitted_by=user.user_id,
            created_at=now,
            updated_at=now,
            **request.model_dump(),
        )
        self.storage.create_daily_submission(submission)
        self._audit(user.user_id, "submission.create", "daily_submission", submission.submission_id, f"Submitted for {department.name}")
        if submission.escalation_required or submission.severe_events > 0:
            self.storage.create_notification(
                NotificationRecord(
                    notification_id=f"NOT-{uuid4().hex[:10].upper()}",
                    created_at=now,
                    user_id=None,
                    scope="facility",
                    title="Escalation required in daily surveillance",
                    message=f"{department.name} reported escalation_required={submission.escalation_required}, severe_events={submission.severe_events}",
                    severity="severe" if submission.severe_events > 0 else "moderate",
                    facility_id=submission.facility_id,
                    entity_type="daily_submission",
                    entity_id=submission.submission_id,
                )
            )
        return submission

    def review_submission(self, submission_id: str, request: SubmissionReviewRequest, user: UserIdentity) -> DailySurveillanceSubmission:
        if user.role not in {"facility_safety_officer", "state_cell_analyst", "national_analyst"}:
            raise PermissionError("User is not allowed to review submissions")
        submission = next((item for item in self.storage.list_daily_submissions() if item.submission_id == submission_id), None)
        if submission is None:
            raise KeyError(submission_id)
        submission.review_status = request.review_status
        submission.reviewed_by = request.reviewed_by
        submission.updated_at = datetime.now(timezone.utc)
        if request.notes:
            submission.notes = f"{submission.notes} | review: {request.notes}".strip(" |")
        self.storage.update_daily_submission(submission)
        self._audit(user.user_id, "submission.review", "daily_submission", submission.submission_id, request.review_status)
        return submission

    def import_facilities(self, request: RegistryImportRequest) -> list[Facility]:
        imported = []
        for record in request.facilities:
            imported.append(self.storage.import_facility(Facility(**record.model_dump())))
        self._audit(request.imported_by, "facility.import", "facility_batch", request.imported_by, f"Imported {len(imported)} facilities")
        return imported

    def triage_report(self, report_id: str, request: TriageRequest, user: UserIdentity) -> EventReport:
        report = self._get_report(report_id)
        if user.role not in {"facility_safety_officer", "state_cell_analyst", "national_analyst"}:
            raise PermissionError("User is not allowed to triage reports")
        report.status = request.status
        report.assigned_to = request.assigned_to
        report.state_cell = request.state_cell
        self.storage.update_report(report)
        self._audit(user.user_id, "report.triage", "report", report.report_id, report.status)
        return report

    def close_report(self, report_id: str, request: ClosureRequest, user: UserIdentity) -> EventReport:
        report = self._get_report(report_id)
        if user.role not in {"facility_safety_officer", "state_cell_analyst", "national_analyst"}:
            raise PermissionError("User is not allowed to close reports")
        report.status = "closed"
        report.closure_note = request.closure_note
        self.storage.update_report(report)
        self._audit(user.user_id, "report.close", "report", report.report_id, request.closure_note)
        return report

    def list_notifications(self, user: UserIdentity) -> list[NotificationRecord]:
        notifications = self.storage.list_notifications(user.user_id)
        if user.role == "facility_safety_officer":
            return [item for item in notifications if item.facility_id in {None, user.facility_id}]
        if user.role == "state_cell_analyst":
            return [item for item in notifications if item.state in {None, user.state}]
        return notifications

    def acknowledge_notification(self, notification_id: str, request: NotificationAcknowledgeRequest, user: UserIdentity) -> NotificationRecord:
        notification = next((item for item in self.storage.list_notifications(user.user_id) if item.notification_id == notification_id), None)
        if notification is None:
            raise KeyError(notification_id)
        notification.status = request.status
        self.storage.update_notification(notification)
        self._audit(user.user_id, "notification.update", "notification", notification_id, request.status)
        return notification

    def list_audit_logs(self, user: UserIdentity, limit: int = 50) -> list[AuditLogRecord]:
        if user.role not in {"governance_admin", "national_analyst", "state_cell_analyst"}:
            raise PermissionError("User is not allowed to view audit logs")
        return self.storage.list_audit_logs(limit)

    def get_trace(self, report_id: str) -> EventTrace:
        report = self._get_report(report_id)
        facility = next(item for item in self.storage.list_facilities() if item.facility_id == report.facility_id)
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
        trend = self.get_trend(user)
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
            trend=trend,
        )

    def get_trend(self, user: UserIdentity) -> TrendSeries:
        facility_id = user.facility_id if user.role in {"facility_reporter", "facility_safety_officer"} else None
        state = user.state if user.role == "state_cell_analyst" else None
        points = self.storage.trend_points(facility_id=facility_id, state=state)
        return TrendSeries(scope=user.role, points=points)

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

    def _identity(self, user: UserRecord) -> UserIdentity:
        return UserIdentity(**user.model_dump(exclude={"password_hash", "password_salt", "created_at", "created_by"}))

    def _get_report(self, report_id: str) -> EventReport:
        report = self.storage.get_report(report_id)
        if report is None:
            raise KeyError(report_id)
        return report

    def _overview(self):
        facilities = self.storage.list_facilities()
        reports = self.storage.list_reports()
        return build_demo_snapshot().overview.model_copy(
            update={
                "facilities_onboarded": len(facilities),
                "states_covered": len({item.state for item in facilities}),
                "reports_received": len(reports),
                "open_investigations": len([item for item in reports if item.status != "closed"]),
                "escalated_signals": len([item for item in self.storage.list_signals() if item.status == "escalated"]),
                "sentinel_events": len([item for item in reports if item.severity == "sentinel"]),
            }
        )

    def _reports_for_user_scope(self, user: UserIdentity) -> list[EventReport]:
        reports = self.storage.list_reports()
        if user.role in {"facility_reporter", "facility_safety_officer"}:
            return [item for item in reports if item.facility_id == user.facility_id]
        if user.role == "state_cell_analyst":
            facility_ids = {item.facility_id for item in self.storage.list_facilities() if item.state == user.state}
            return [item for item in reports if item.facility_id in facility_ids]
        return reports

    def _audit(self, actor_user_id: str | None, action: str, entity_type: str, entity_id: str, detail: str) -> None:
        self.storage.create_audit_log(
            AuditLogRecord(
                audit_id=f"AUD-{uuid4().hex[:10].upper()}",
                created_at=datetime.now(timezone.utc),
                actor_user_id=actor_user_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                detail=detail,
            )
        )
