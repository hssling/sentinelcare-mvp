from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone
from uuid import uuid4

from .ai import assist_with_model, encrypt_api_key, mask_api_key, provider_catalog
from .contracts import (
    AIAssistRequest,
    AIAssistResponse,
    AIProviderConfigCreate,
    AIProviderConfigStored,
    AIProviderConfigView,
    AuditLogRecord,
    ClosureRequest,
    DailySubmissionCreate,
    DailySurveillanceSubmission,
    DashboardAlert,
    DashboardIndicator,
    DashboardSnapshot,
    Department,
    EventCase,
    EventCaseCreate,
    EventCaseReviewRequest,
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
        return SurveillanceSnapshot(
            overview=self._overview(),
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
            request.state = current_user.state
            request.district = current_user.district
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
            facility_ids = self._facility_ids_for_state(user.state)
            return [item for item in submissions if item.facility_id in facility_ids]
        return submissions

    def list_reports(self, user: UserIdentity) -> list[EventReport]:
        return self._reports_for_user_scope(user)

    def list_event_cases(self, user: UserIdentity) -> list[EventCase]:
        cases = self.storage.list_event_cases()
        if user.role == "facility_reporter":
            return [item for item in cases if item.department_id == user.department_id]
        if user.role == "facility_safety_officer":
            return [item for item in cases if item.facility_id == user.facility_id]
        if user.role == "state_cell_analyst":
            facility_ids = self._facility_ids_for_state(user.state)
            return [item for item in cases if item.facility_id in facility_ids]
        return cases

    def create_daily_submission(self, request: DailySubmissionCreate, user: UserIdentity) -> DailySurveillanceSubmission:
        if user.role not in {"facility_reporter", "facility_safety_officer"}:
            raise PermissionError("User is not allowed to submit daily surveillance data")
        department = self._department(request.department_id)
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

    def create_event_case(self, request: EventCaseCreate, user: UserIdentity) -> EventCase:
        if user.role not in {"facility_reporter", "facility_safety_officer", "district_reviewer", "state_cell_analyst", "national_analyst"}:
            raise PermissionError("User is not allowed to create event cases")
        department = self._department(request.department_id)
        if user.facility_id and department.facility_id != user.facility_id:
            raise PermissionError("Department does not belong to the user's facility")
        now = datetime.now(timezone.utc)
        event_case = EventCase(
            case_id=f"CASE-{uuid4().hex[:10].upper()}",
            facility_id=department.facility_id,
            created_at=now,
            updated_at=now,
            due_date=(now + timedelta(days=7)).date(),
            **request.model_dump(),
        )
        self.storage.create_event_case(event_case)
        self._audit(user.user_id, "case.create", "event_case", event_case.case_id, event_case.event_summary)
        if event_case.severity_level in {"severe", "sentinel"}:
            self.storage.create_notification(
                NotificationRecord(
                    notification_id=f"NOT-{uuid4().hex[:10].upper()}",
                    created_at=now,
                    user_id=None,
                    scope="facility",
                    title="High-severity event case created",
                    message=f"{event_case.case_id} requires escalation review for {event_case.severity_level} severity.",
                    severity=event_case.severity_level,
                    facility_id=event_case.facility_id,
                    entity_type="event_case",
                    entity_id=event_case.case_id,
                )
            )
        return event_case

    def review_event_case(self, case_id: str, request: EventCaseReviewRequest, user: UserIdentity) -> EventCase:
        if user.role not in {"facility_safety_officer", "district_reviewer", "state_cell_analyst", "national_analyst"}:
            raise PermissionError("User is not allowed to review event cases")
        event_case = self.storage.get_event_case(case_id)
        if event_case is None:
            raise KeyError(case_id)
        event_case.triage_status = request.triage_status
        event_case.owner_assigned = request.owner_assigned
        event_case.investigation_method = request.investigation_method
        event_case.root_cause_category = request.root_cause_category
        event_case.corrective_action = request.corrective_action
        event_case.preventive_action = request.preventive_action
        event_case.due_date = request.due_date
        event_case.closure_status = request.closure_status
        event_case.closure_quality_rating = request.closure_quality_rating
        event_case.ai_human_override = request.ai_human_override
        event_case.updated_at = datetime.now(timezone.utc)
        if request.closure_status == "closed":
            event_case.closure_date = date.today()
        self.storage.update_event_case(event_case)
        self._audit(user.user_id, "case.review", "event_case", case_id, request.triage_status)
        return event_case

    def list_ai_provider_catalog(self):
        return provider_catalog()

    def list_ai_provider_configs(self, user: UserIdentity) -> list[AIProviderConfigView]:
        return [self._config_view(item) for item in self.storage.list_ai_provider_configs(user.user_id)]

    def upsert_ai_provider_config(self, request: AIProviderConfigCreate, user: UserIdentity) -> AIProviderConfigView:
        now = datetime.now(timezone.utc)
        existing = self.storage.get_active_ai_provider_config(user.user_id)
        config = AIProviderConfigStored(
            config_id=existing.config_id if existing and existing.provider == request.provider else f"AICFG-{uuid4().hex[:10].upper()}",
            owner_user_id=user.user_id,
            provider=request.provider,
            label=request.label,
            model=request.model,
            base_url=request.base_url or next(item.default_base_url for item in provider_catalog() if item.provider == request.provider),
            api_key_ciphertext=encrypt_api_key(request.api_key),
            api_key_masked=mask_api_key(request.api_key),
            is_active=request.is_active,
            created_at=existing.created_at if existing and existing.provider == request.provider else now,
            updated_at=now,
        )
        self.storage.upsert_ai_provider_config(config)
        self._audit(user.user_id, "ai.config.upsert", "ai_provider_config", config.config_id, f"{config.provider}:{config.model}")
        return self._config_view(config)

    def ai_assist_case(self, request: AIAssistRequest, user: UserIdentity) -> AIAssistResponse:
        config = self.storage.get_active_ai_provider_config(user.user_id)
        if config is None:
            raise PermissionError("No active AI provider configuration found for this user")
        response = assist_with_model(config, request)
        if request.case_id:
            event_case = self.storage.get_event_case(request.case_id)
            if event_case:
                event_case.ai_summary = response.summary
                event_case.ai_confidence = response.confidence
                event_case.ai_provider = response.provider
                event_case.ai_model = response.model
                if response.structured_fields.get("corrective_action") and not event_case.corrective_action:
                    event_case.corrective_action = str(response.structured_fields["corrective_action"])
                if response.structured_fields.get("preventive_action") and not event_case.preventive_action:
                    event_case.preventive_action = str(response.structured_fields["preventive_action"])
                event_case.updated_at = datetime.now(timezone.utc)
                self.storage.update_event_case(event_case)
        self._audit(user.user_id, "ai.assist", "event_case", request.case_id or "ad_hoc", f"{response.provider}:{response.model}")
        return response

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
        linked_case = next((item for item in self.storage.list_event_cases() if item.report_id == report.report_id), None)
        return EventTrace(
            report_id=report.report_id,
            facility=facility.name,
            state=facility.state,
            district=facility.district,
            domain=report.domain,
            deviation_class=report.deviation_class,
            severity=report.severity,
            validation_phase="controlled_pilot",
            active_policy_version=linked_case.linked_policy_version if linked_case and linked_case.linked_policy_version else "National minimum dataset v1 / signal rules pilot set",
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
                    step="case_linkage",
                    finding=linked_case.case_id if linked_case else "No event-level case linked yet",
                    output="Manual and machine streams harmonized for national learning.",
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
        cases = self.list_event_cases(user)
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
        if any(item.severity_level in {"severe", "sentinel"} for item in cases):
            alerts.append(
                DashboardAlert(
                    alert_id="ALERT-CASE-001",
                    severity="severe",
                    title="High-risk event cases require CAPA review",
                    detail="At least one severe or sentinel event case remains open in your scope.",
                    owner_role="State cell analyst" if user.role != "facility_reporter" else "Facility safety officer",
                )
            )
        trend = self.get_trend(user)
        return DashboardSnapshot(
            scope=user.role,
            indicators=[
                DashboardIndicator(label="Daily submissions", value=len(submissions), trend="stable"),
                DashboardIndicator(label="Pending review", value=len([s for s in submissions if s.review_status == "submitted"]), trend="watch"),
                DashboardIndicator(label="Open reports", value=len([r for r in reports if r.status != "closed"]), trend="watch"),
                DashboardIndicator(label="Open event cases", value=len([c for c in cases if c.closure_status != "closed"]), trend="watch"),
                DashboardIndicator(label="Sentinel/severe cases", value=len([c for c in cases if c.severity_level in {"severe", "sentinel"}]), trend="up"),
                DashboardIndicator(label="Learning actions due", value=len([c for c in cases if c.due_date and c.closure_status != "closed"]), trend="up"),
            ],
            alerts=alerts,
            submissions_pending_review=len([s for s in submissions if s.review_status == "submitted"]),
            reports_open=len([r for r in reports if r.status != "closed"]),
            event_cases_open=len([c for c in cases if c.closure_status != "closed"]),
            learning_actions_due=len([c for c in cases if c.due_date and c.closure_status != "closed"]),
            trend=trend,
        )

    def get_trend(self, user: UserIdentity) -> TrendSeries:
        facility_id = user.facility_id if user.role in {"facility_reporter", "facility_safety_officer"} else None
        state = user.state if user.role == "state_cell_analyst" else None
        points = self.storage.trend_points(facility_id=facility_id, state=state)
        domain_breakdown = self.storage.domain_breakdown(facility_id=facility_id, state=state)
        return TrendSeries(scope=user.role, points=points, domain_breakdown=domain_breakdown)

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
                "SentinelCare live clinical workflow intelligence layer",
            ],
            input_modes=["web form", "CSV upload", "FHIR API", "HL7 feed", "manual state batch submission", "SentinelCare alert intake"],
            standards=["FHIR", "HL7 v2", "CSV templates", "canonical surveillance JSON schema"],
            privacy_controls=[
                "role-based access control",
                "de-identification above facility tier",
                "audit trail",
                "minimum necessary identifiers",
                "encrypted user-supplied AI API keys",
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

    def _config_view(self, config: AIProviderConfigStored) -> AIProviderConfigView:
        return AIProviderConfigView(**config.model_dump(exclude={"api_key_ciphertext"}))

    def _department(self, department_id: str) -> Department:
        department = next((item for item in self.storage.list_departments() if item.department_id == department_id), None)
        if department is None:
            raise KeyError(department_id)
        return department

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
                "sentinel_events": len([item for item in self.storage.list_event_cases() if item.severity_level == "sentinel"]),
            }
        )

    def _reports_for_user_scope(self, user: UserIdentity) -> list[EventReport]:
        reports = self.storage.list_reports()
        if user.role in {"facility_reporter", "facility_safety_officer"}:
            return [item for item in reports if item.facility_id == user.facility_id]
        if user.role == "state_cell_analyst":
            facility_ids = self._facility_ids_for_state(user.state)
            return [item for item in reports if item.facility_id in facility_ids]
        return reports

    def _facility_ids_for_state(self, state: str | None) -> set[str]:
        return {item.facility_id for item in self.storage.list_facilities() if item.state == state}

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
