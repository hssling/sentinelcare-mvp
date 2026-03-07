from __future__ import annotations

import json

from .demo_data import capability_demo_events, demo_events
from .pipeline import SentinelCarePipeline


def main() -> None:
    pipeline = SentinelCarePipeline()
    capability = pipeline.run_capability_demo(capability_demo_events())
    print(json.dumps({"capability_demo": capability}, indent=2))

    print(json.dumps({"baseline_demo": pipeline.run_full_workflow(demo_events())}, indent=2))

    policy = pipeline.submit_policy(
        policy_name="critical_result_closure_policy",
        definition={"ack_timeout_minutes": 30, "escalate_after_minutes": 45},
        submitted_by="quality_lead",
    )
    approved = pipeline.approve_policy(policy.policy_id, approved_by="governance_chair")
    validation = pipeline.generate_validation_report()
    print(
        json.dumps(
            {
                "governance_and_validation": {
                    "submitted_policy": policy.model_dump(mode="json"),
                    "approved_policy": approved.model_dump(mode="json"),
                    "validation_report": validation.model_dump(mode="json"),
                    "workflow_queue_open": len([q for q in pipeline.list_queue() if q.status == "open"]),
                }
            },
            indent=2,
        )
    )

    result = pipeline.process_events(demo_events())
    if result.alerts:
        first_alert = result.alerts[-1]
        action = pipeline.record_review_action(
            alert_id=first_alert.alert_id,
            acted_by="nurse_001",
            action_type="acknowledged_and_actioned",
            comment="Action initiated from command line demo.",
        )
        print(
            json.dumps(
                {
                    "review_action_recorded": action.model_dump(mode="json"),
                    "updated_alert_status": pipeline.alert_store[first_alert.alert_id].status,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
