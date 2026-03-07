from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .contracts import Event
from .demo_data import demo_events
from .pipeline import SentinelCarePipeline

app = FastAPI(title="SentinelCare MVP API", version="0.1.0")
pipeline = SentinelCarePipeline()


class ReviewActionRequest(BaseModel):
    alert_id: str
    acted_by: str
    action_type: str
    override_reason: str | None = None
    comment: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/events/process")
def process_event(event: Event) -> dict:
    result = pipeline.process_event(event)
    return {
        "alerts_generated": len(result.alerts),
        "alerts": [a.model_dump(mode="json") for a in result.alerts],
        "tasks": [t.model_dump(mode="json") for t in result.tasks],
    }


@app.post("/demo/run")
def run_demo() -> dict:
    result = pipeline.process_events(demo_events())
    return {
        "alerts_generated": len(result.alerts),
        "task_count": len(result.tasks),
        "domains": sorted({a.domain for a in result.alerts}),
        "alerts": [a.model_dump(mode="json") for a in result.alerts],
    }


@app.post("/alerts/review")
def review_alert(request: ReviewActionRequest) -> dict:
    action = pipeline.record_review_action(
        alert_id=request.alert_id,
        acted_by=request.acted_by,
        action_type=request.action_type,
        override_reason=request.override_reason,
        comment=request.comment,
    )
    return {"review_action": action.model_dump(mode="json")}


@app.get("/metrics/summary")
def metrics_summary() -> dict:
    return pipeline.summary()


def run() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
