from __future__ import annotations

from fastapi import Header, HTTPException

from .contracts import UserIdentity
from .service import IndiaSurveillanceService


def resolve_user(service: IndiaSurveillanceService, x_demo_user: str | None) -> UserIdentity:
    user_id = x_demo_user or "demo-national"
    try:
        return service.get_user(user_id)
    except KeyError as exc:
        raise HTTPException(status_code=401, detail=f"Unknown demo user: {user_id}") from exc


def demo_user_header(x_demo_user: str | None = Header(default=None)) -> str | None:
    return x_demo_user
