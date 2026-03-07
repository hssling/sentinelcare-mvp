from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .auth import demo_user_header, resolve_user
from .contracts import ClosureRequest, RegistryImportRequest, TriageRequest
from .service import IndiaSurveillanceService

service = IndiaSurveillanceService()
app = FastAPI(title="India Patient Safety Surveillance System", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/overview")
def overview():
    return service.get_snapshot().overview


@app.get("/facilities")
def facilities():
    return service.get_snapshot().facilities


@app.get("/reports")
def reports():
    return service.get_snapshot().reports


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
