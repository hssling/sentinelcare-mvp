from __future__ import annotations

import json

from .demo_data import demo_events
from .pipeline import SentinelCarePipeline


def main() -> None:
    pipeline = SentinelCarePipeline()
    result = pipeline.process_events(demo_events())

    output = {
        "alerts_generated": len(result.alerts),
        "task_count": len(result.tasks),
        "domains": sorted({a.domain for a in result.alerts}),
    }
    print(json.dumps(output, indent=2))

    if result.alerts:
        first_alert = result.alerts[0]
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
