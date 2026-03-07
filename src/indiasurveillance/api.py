from __future__ import annotations

import os

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .auth import session_header
from .contracts import (
    AIAssistRequest,
    AIProviderConfigCreate,
    ClosureRequest,
    DailySubmissionCreate,
    EventCaseCreate,
    EventCaseReviewRequest,
    LoginRequest,
    NotificationAcknowledgeRequest,
    RegistryImportRequest,
    SubmissionReviewRequest,
    TriageRequest,
    UserCreateRequest,
)
from .service import IndiaSurveillanceService

service = IndiaSurveillanceService()
app = FastAPI(title="India Patient Safety Surveillance System", version="0.4.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://mederror-india-surveillance.netlify.app",
        os.getenv("INDIA_SURVEILLANCE_ALLOWED_ORIGIN", ""),
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


def session_user(token: str | None = Depends(session_header)):
    try:
        return service.resolve_session(token)
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@app.post("/auth/login")
def login(request: LoginRequest):
    try:
        return service.login(request)
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@app.get("/me")
def me(user=Depends(session_user)):
    return user


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/overview")
def overview():
    return service.get_snapshot().overview


@app.get("/facilities")
def facilities():
    return service.get_snapshot().facilities


@app.get("/departments")
def departments(facility_id: str | None = None, user=Depends(session_user)):
    return service.list_departments(user, facility_id)


@app.get("/reports")
def reports(user=Depends(session_user)):
    return service.list_reports(user)


@app.get("/event-cases")
def event_cases(user=Depends(session_user)):
    return service.list_event_cases(user)


@app.post("/event-cases")
def create_event_case(request: EventCaseCreate, user=Depends(session_user)):
    try:
        return service.create_event_case(request, user)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown department_id: {exc.args[0]}") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.post("/event-cases/{case_id}/review")
def review_event_case(case_id: str, request: EventCaseReviewRequest, user=Depends(session_user)):
    try:
        return service.review_event_case(case_id, request, user)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown case_id: {exc.args[0]}") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.get("/daily-submissions")
def daily_submissions(user=Depends(session_user)):
    return service.list_daily_submissions(user)


@app.post("/daily-submissions")
def create_daily_submission(request: DailySubmissionCreate, user=Depends(session_user)):
    try:
        return service.create_daily_submission(request, user)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown department_id: {exc.args[0]}") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.post("/daily-submissions/{submission_id}/review")
def review_daily_submission(submission_id: str, request: SubmissionReviewRequest, user=Depends(session_user)):
    try:
        return service.review_submission(submission_id, request, user)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown submission_id: {exc.args[0]}") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.get("/dashboard")
def dashboard(user=Depends(session_user)):
    return service.get_dashboard(user)


@app.get("/trends")
def trends(user=Depends(session_user)):
    return service.get_trend(user)


@app.get("/signals")
def signals():
    return service.get_snapshot().signals


@app.get("/policies")
def policies():
    return service.get_snapshot().policies


@app.get("/users")
def users(user=Depends(session_user)):
    return service.list_users(user)


@app.post("/users")
def create_user(request: UserCreateRequest, user=Depends(session_user)):
    try:
        return service.create_user(request, user)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.get("/state-cells")
def state_cells():
    return service.list_state_cells()


@app.get("/snapshot")
def snapshot():
    return service.get_snapshot()


@app.get("/trace/{report_id}")
def trace(report_id: str):
    try:
        return service.get_trace(report_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown report_id: {report_id}") from exc


@app.get("/notifications")
def notifications(user=Depends(session_user)):
    return service.list_notifications(user)


@app.post("/notifications/{notification_id}/acknowledge")
def acknowledge_notification(notification_id: str, request: NotificationAcknowledgeRequest, user=Depends(session_user)):
    try:
        return service.acknowledge_notification(notification_id, request, user)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown notification_id: {exc.args[0]}") from exc


@app.get("/audit-logs")
def audit_logs(limit: int = Query(default=50, ge=1, le=200), user=Depends(session_user)):
    try:
        return service.list_audit_logs(user, limit)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.get("/integration-profile")
def integration_profile():
    return service.get_integration_profile()


@app.post("/registry/import")
def registry_import(request: RegistryImportRequest, user=Depends(session_user)):
    if user.role not in {"state_cell_analyst", "national_analyst", "governance_admin"}:
        raise HTTPException(status_code=403, detail="User is not allowed to import facilities")
    return service.import_facilities(request)


@app.post("/reports/{report_id}/triage")
def triage_report(report_id: str, request: TriageRequest, user=Depends(session_user)):
    try:
        return service.triage_report(report_id, request, user)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown report_id: {report_id}") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.post("/reports/{report_id}/close")
def close_report(report_id: str, request: ClosureRequest, user=Depends(session_user)):
    try:
        return service.close_report(report_id, request, user)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown report_id: {report_id}") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.get("/ai/providers")
def ai_provider_catalog(user=Depends(session_user)):
    return {
        "catalog": service.list_ai_provider_catalog(),
        "configs": service.list_ai_provider_configs(user),
    }


@app.post("/ai/providers")
def upsert_ai_provider(request: AIProviderConfigCreate, user=Depends(session_user)):
    return service.upsert_ai_provider_config(request, user)


@app.post("/ai/assist")
def ai_assist(request: AIAssistRequest, user=Depends(session_user)):
    try:
        return service.ai_assist_case(request, user)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/sources")
def sources() -> dict[str, list[str]]:
    return {
        "official_sources": [
            "https://www.abdm.gov.in/resources",
            "https://hfr.abdm.gov.in/",
            "https://ihip.mohfw.gov.in/",
            "https://nhm.gov.in/",
            "https://ipc.gov.in/PvPI/about.html",
            "https://nabh.co/nabh-standards/",
            "https://platform.openai.com/api-keys",
            "https://console.anthropic.com/settings/keys",
            "https://aistudio.google.com/app/apikey",
            "https://openrouter.ai/settings/keys",
            "https://console.groq.com/keys",
            "https://api.together.xyz/settings/api-keys",
            "https://dashboard.cohere.com/api-keys",
            "https://console.x.ai/",
        ]
    }


def run() -> None:
    import uvicorn

    uvicorn.run("indiasurveillance.api:app", host="0.0.0.0", port=8010, reload=False)
