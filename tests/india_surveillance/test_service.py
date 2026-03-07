from indiasurveillance.service import IndiaSurveillanceService
from indiasurveillance.contracts import ClosureRequest, FacilityImportRecord, RegistryImportRequest, TriageRequest


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
    assert trace.trace_steps[0].step == 'input'


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
