from sentinelcare.demo_data import demo_events
from sentinelcare.pipeline import SentinelCarePipeline


def test_end_to_end_generates_all_domain_alerts() -> None:
    pipeline = SentinelCarePipeline()
    result = pipeline.process_events(demo_events())

    domains = {alert.domain for alert in result.alerts}
    assert "medication_safety" in domains
    assert "critical_result_closure" in domains
    assert "deterioration_surveillance" in domains
    assert len(result.tasks) >= len(demo_events()) * 8


def test_review_action_closes_alert() -> None:
    pipeline = SentinelCarePipeline()
    result = pipeline.process_events(demo_events())
    alert = result.alerts[0]

    action = pipeline.record_review_action(
        alert_id=alert.alert_id,
        acted_by="doctor_001",
        action_type="resolved",
        comment="Handled in test",
    )

    assert action.alert_id == alert.alert_id
    assert pipeline.alert_store[alert.alert_id].status == "closed"


def test_summary_contains_counts() -> None:
    pipeline = SentinelCarePipeline()
    pipeline.process_events(demo_events())
    summary = pipeline.summary()
    assert summary["events_total"] == 3
    assert summary["alerts_total"] >= 3
    assert summary["agent_catalog_size"] == 8
    assert "medication_safety" in summary["alerts_by_domain"]


def test_agent_catalog_and_single_run() -> None:
    pipeline = SentinelCarePipeline()
    catalog = pipeline.get_agent_catalog()
    assert len(catalog) == 8
    assert catalog[0]["agent_id"] == "A"

    outcome = pipeline.run_single_agent("D", demo_events()[0])
    assert outcome["agent_id"] == "D"
    assert len(outcome["tasks"]) == 2
