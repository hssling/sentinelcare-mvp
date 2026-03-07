from __future__ import annotations

from fastapi import Header


def session_header(authorization: str | None = Header(default=None)) -> str | None:
    if not authorization:
        return None
    if authorization.lower().startswith("bearer "):
        return authorization[7:]
    return authorization
