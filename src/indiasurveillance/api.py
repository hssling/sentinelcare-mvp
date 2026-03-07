from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .auth import demo_user_header, resolve_user, session_header
from .contracts import (
    ClosureRequest,
    DailySubmissionCreate,
    LoginRequest,
    RegistryImportRequest,
    SubmissionReviewRequest,
    TriageRequest,
)
from .service import IndiaSurveillanceService

service = IndiaSurveillanceService()
app = FastAPI(title="India Patient Safety Surveillance System", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    if user.role in {"facility_reporter", "facility_safety_officer"}:
        facility_id = user.facility_id
    return service.list_departments(facility_id)


@app.get("/reports")
def reports():
    return service.get_snapshot().reports


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


@app.get("/signals")
def signals():
    return service.get_snapshot().signals


@app.get("/policies")
def policies():
    return service.get_snapshot().policies


@app.get("/users")
def users():
    return service.list_users()


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


@app.get("/integration-profile")
def integration_profile():
    return service.get_integration_profile()


@app.post("/registry/import")
def registry_import(
    request: RegistryImportRequest,
    x_demo_user: str | None = Depends(demo_user_header),
):
    user = resolve_user(service, x_demo_user)
    if user.role not in {"state_cell_analyst", "national_analyst", "governance_admin"}:
        raise HTTPException(status_code=403, detail="User is not allowed to import facilities")
    return service.import_facilities(request)


@app.post("/reports/{report_id}/triage")
def triage_report(
    report_id: str,
    request: TriageRequest,
    x_demo_user: str | None = Depends(demo_user_header),
):
    user = resolve_user(service, x_demo_user)
    try:
        return service.triage_report(report_id, request, user)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown report_id: {report_id}") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.post("/reports/{report_id}/close")
def close_report(
    report_id: str,
    request: ClosureRequest,
    x_demo_user: str | None = Depends(demo_user_header),
):
    user = resolve_user(service, x_demo_user)
    try:
        return service.close_report(report_id, request, user)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown report_id: {report_id}") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


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
        ]
    }


def run() -> None:
    import uvicorn

    uvicorn.run("indiasurveillance.api:app", host="0.0.0.0", port=8010, reload=False)
