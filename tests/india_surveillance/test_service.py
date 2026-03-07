from datetime import date

from indiasurveillance.contracts import (
    ClosureRequest,
    DailySubmissionCreate,
    FacilityImportRecord,
    LoginRequest,
    RegistryImportRequest,
    SubmissionReviewRequest,
    TriageRequest,
)
from indiasurveillance.service import IndiaSurveillanceService


def test_snapshot_has_reports_and_signals():
    service = IndiaSurveillanceService()
    snapshot = service.get_snapshot()
    assert snapshot.overview.reports_received >= len(snapshot.reports)
    assert len(snapshot.signals) >= 1


def test_trace_contains_explainable_steps():
    service = IndiaSurveillanceService()
    report_id = service.get_snapshot().reports[0].report_id
    trace = service.get_trace(report_id)
    assert trace.report_id == report_id
    assert len(trace.trace_steps) >= 4
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


def test_login_submission_review_and_dashboard_flow():
    service = IndiaSurveillanceService()
    session = service.login(LoginRequest(username="tmk-ed", password="pass123"))
    user = service.resolve_session(session.access_token)
    submission = service.create_daily_submission(
        DailySubmissionCreate(
            submission_date=date(2026, 3, 8),
            department_id="DEPT-TMK-ED",
            patient_days=120,
            near_misses=3,
            no_harm_events=1,
            harm_events=1,
            severe_events=0,
            medication_events=1,
            procedure_events=0,
            infection_events=0,
            diagnostic_events=1,
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
    assert len(dashboard.indicators) >= 3
