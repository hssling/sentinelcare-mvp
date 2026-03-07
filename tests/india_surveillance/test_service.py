from datetime import date, datetime, timezone

from indiasurveillance.contracts import (
    AIProviderConfigCreate,
    ClosureRequest,
    DailySubmissionCreate,
    EventCaseCreate,
    EventCaseReviewRequest,
    FacilityImportRecord,
    LoginRequest,
    NotificationAcknowledgeRequest,
    RegistryImportRequest,
    SubmissionReviewRequest,
    TriageRequest,
    UserCreateRequest,
)
from indiasurveillance.service import IndiaSurveillanceService


def test_snapshot_has_reports_signals_and_cases():
    service = IndiaSurveillanceService()
    snapshot = service.get_snapshot()
    assert snapshot.overview.reports_received >= len(snapshot.reports)
    assert len(snapshot.signals) >= 1
    assert len(service.list_event_cases(service.get_user("demo-national"))) >= 1


def test_trace_contains_explainable_steps():
    service = IndiaSurveillanceService()
    report_id = service.get_snapshot().reports[0].report_id
    trace = service.get_trace(report_id)
    assert trace.report_id == report_id
    assert len(trace.trace_steps) >= 5
    assert trace.trace_steps[0].step == "input"


def test_registry_import_increases_facility_count():
    service = IndiaSurveillanceService()
    before = len(service.get_snapshot().facilities)
    service.import_facilities(
        RegistryImportRequest(
            imported_by="demo-national",
            facilities=[
                FacilityImportRecord(
                    facility_id="FAC-KA-NEW-01",
                    name="Karnataka Pilot District Hospital",
                    state="Karnataka",
                    district="Mysuru",
                    ownership="public",
                    level="district_hospital",
                    abdm_registry_ready=True,
                )
            ],
        )
    )
    assert len(service.get_snapshot().facilities) == before + 1


def test_triage_and_close_workflow_updates_report():
    service = IndiaSurveillanceService()
    user = service.get_user("demo-state-ka")
    report = service.triage_report(
        "EVT-IND-1003",
        TriageRequest(status="investigating", assigned_to="Karnataka State Cell Analyst", state_cell="Karnataka state cell"),
        user,
    )
    assert report.status == "investigating"
    closed = service.close_report(
        "EVT-IND-1003",
        ClosureRequest(closure_note="Reviewed at state cell and CAPA issued."),
        user,
    )
    assert closed.status == "closed"
    assert closed.closure_note is not None


def test_login_submission_review_dashboard_notification_and_audit_flow():
    service = IndiaSurveillanceService()
    session = service.login(LoginRequest(username="tmk-ed", password="pass123"))
    assert session.token_type == "bearer"
    user = service.resolve_session(session.access_token)
    submission = service.create_daily_submission(
        DailySubmissionCreate(
            submission_date=date(2026, 3, 8),
            department_id="DEPT-TMK-ED",
            patient_days=120,
            admissions=45,
            discharges=38,
            critical_results_count=3,
            near_misses=3,
            no_harm_events=1,
            harm_events=1,
            severe_events=1,
            medication_events=1,
            procedure_events=0,
            infection_events=0,
            diagnostic_events=1,
            escalation_required=True,
            notes="Routine daily feed.",
        ),
        user,
    )
    assert submission.submitted_by == user.user_id

    manager = service.get_user("demo-fso-ka")
    reviewed = service.review_submission(
        submission.submission_id,
        SubmissionReviewRequest(review_status="reviewed", reviewed_by=manager.name, notes="Reviewed in facility huddle"),
        manager,
    )
    assert reviewed.review_status == "reviewed"

    dashboard = service.get_dashboard(manager)
    assert dashboard.submissions_pending_review >= 0
    assert len(dashboard.indicators) >= 5
    assert dashboard.trend is not None

    notifications = service.list_notifications(manager)
    assert len(notifications) >= 1
    updated = service.acknowledge_notification(
        notifications[0].notification_id,
        NotificationAcknowledgeRequest(status="acknowledged"),
        manager,
    )
    assert updated.status == "acknowledged"

    audits = service.list_audit_logs(service.get_user("demo-national"))
    assert any(item.action == "submission.create" for item in audits)


def test_admin_can_create_user_and_login():
    service = IndiaSurveillanceService()
    admin = service.get_user("demo-admin")
    created = service.create_user(
        UserCreateRequest(
            name="New ED Reporter",
            username="new-ed",
            password="pass123",
            role="facility_reporter",
            facility_id="FAC-TMK-001",
            department_id="DEPT-TMK-ED",
            state="Karnataka",
            district="Tumkur",
        ),
        admin,
    )
    assert created.username == "new-ed"

    session = service.login(LoginRequest(username="new-ed", password="pass123"))
    assert session.user.user_id == created.user_id


def test_event_case_creation_review_and_ai_config():
    service = IndiaSurveillanceService()
    reporter = service.get_user("demo-ed-ka")
    event_case = service.create_event_case(
        EventCaseCreate(
            department_id="DEPT-TMK-ED",
            event_timestamp=datetime(2026, 3, 8, 10, 15, tzinfo=timezone.utc),
            encounter_setting="emergency",
            shift="morning",
            patient_age_band="18-44",
            patient_sex="female",
            domain="diagnostic",
            deviation_class="harmful_delay",
            process_stage="test -> result -> action",
            event_type="critical result callback delay",
            actual_harm="Delayed treatment decision",
            potential_harm="Escalation to severe deterioration",
            severity_level="moderate",
            event_summary="Critical result callback delayed during peak handover.",
            what_was_expected="Critical result should trigger clinician acknowledgment within target window.",
            what_happened="Callback escalated late and action was delayed.",
            immediate_action_taken="On-call registrar contacted and patient recalled.",
            evidence_source="manual narrative",
            contributing_factors=["handover_communication", "staffing_workload"],
        ),
        reporter,
    )
    assert event_case.case_id.startswith("CASE-")

    reviewer = service.get_user("demo-fso-ka")
    reviewed = service.review_event_case(
        event_case.case_id,
        EventCaseReviewRequest(
            triage_status="investigating",
            owner_assigned=reviewer.name,
            investigation_method="mini RCA",
            root_cause_category="handover failure",
            corrective_action="Escalation checklist introduced.",
            preventive_action="Critical result acknowledgment timer deployed.",
            closure_status="open",
        ),
        reviewer,
    )
    assert reviewed.owner_assigned == reviewer.name

    config = service.upsert_ai_provider_config(
        AIProviderConfigCreate(
            provider="openai",
            label="Ops classification",
            model="gpt-4.1-mini",
            api_key="sk-test-1234567890",
        ),
        reviewer,
    )
    assert config.api_key_masked.startswith("sk-t")
    assert len(service.list_ai_provider_configs(reviewer)) == 1
