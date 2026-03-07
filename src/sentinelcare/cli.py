from __future__ import annotations

import json

from .demo_data import capability_demo_events, demo_events
from .pipeline import SentinelCarePipeline


def main() -> None:
    pipeline = SentinelCarePipeline()
    capability = pipeline.run_capability_demo(capability_demo_events())
    print(json.dumps({"capability_demo": capability}, indent=2))

    print(json.dumps({"baseline_demo": pipeline.run_full_workflow(demo_events())}, indent=2))

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
