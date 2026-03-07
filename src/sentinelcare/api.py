from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .contracts import Event
from .demo_data import capability_demo_events, demo_events
from .pipeline import SentinelCarePipeline

app = FastAPI(title="SentinelCare MVP API", version="0.1.0")
pipeline = SentinelCarePipeline()


class ReviewActionRequest(BaseModel):
    alert_id: str
    acted_by: str
    action_type: str
    override_reason: str | None = None
    comment: str | None = None


class AgentRunRequest(BaseModel):
    agent_id: str
    event: Event


class PolicySubmitRequest(BaseModel):
    policy_name: str
    definition: dict
    submitted_by: str


class PolicyApproveRequest(BaseModel):
    approved_by: str


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
    return pipeline.run_full_workflow(demo_events())


@app.get("/demo/scenarios")
def demo_scenarios() -> dict:
    return {
        "scenarios": [
            {"name": "baseline_mixed", "event_count": len(demo_events())},
            {"name": "capability_showcase", "event_count": len(capability_demo_events())},
        ]
    }


@app.post("/demo/capability-run")
def run_capability_demo() -> dict:
    return pipeline.run_capability_demo(capability_demo_events())


@app.get("/agents/catalog")
def agents_catalog() -> dict:
    return {"agents": pipeline.get_agent_catalog()}


@app.post("/agents/run")
def run_single_agent(request: AgentRunRequest) -> dict:
    try:
        return pipeline.run_single_agent(request.agent_id, request.event)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


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


@app.get("/workflow/queue")
def workflow_queue(status: str | None = None) -> dict:
    return {"items": [i.model_dump(mode="json") for i in pipeline.list_queue(status)]}


@app.post("/workflow/queue/escalate")
def escalate_queue() -> dict:
    return pipeline.escalate_overdue_queue()


@app.post("/governance/policies/submit")
def submit_policy(request: PolicySubmitRequest) -> dict:
    policy = pipeline.submit_policy(request.policy_name, request.definition, request.submitted_by)
    return {"policy": policy.model_dump(mode="json")}


@app.post("/governance/policies/{policy_id}/approve")
def approve_policy(policy_id: str, request: PolicyApproveRequest) -> dict:
    try:
        policy = pipeline.approve_policy(policy_id, request.approved_by)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"policy": policy.model_dump(mode="json")}


@app.get("/governance/policies")
def list_policies(status: str | None = None) -> dict:
    return {"policies": [p.model_dump(mode="json") for p in pipeline.list_policies(status)]}


@app.post("/validation/report")
def create_validation_report(report_type: str = "operational_validation") -> dict:
    report = pipeline.generate_validation_report(report_type=report_type)
    return {"report": report.model_dump(mode="json")}


@app.get("/validation/reports")
def list_validation_reports() -> dict:
    return {"reports": [r.model_dump(mode="json") for r in pipeline.list_validation_reports()]}


def run() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
