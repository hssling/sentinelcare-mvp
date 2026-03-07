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
    assert trace.trace_steps[0].step == 'input'
