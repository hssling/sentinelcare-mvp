from __future__ import annotations

import json

from .service import IndiaSurveillanceService


def main() -> None:
    service = IndiaSurveillanceService()
    snapshot = service.get_snapshot()
    payload = {
        "overview": snapshot.overview.model_dump(),
        "report_count": len(snapshot.reports),
        "signal_count": len(snapshot.signals),
        "policy_count": len(snapshot.policies),
        "sample_trace": service.get_trace(snapshot.reports[0].report_id).model_dump(),
    }
    print(json.dumps(payload, indent=2, default=str))


if __name__ == "__main__":
    main()
