from __future__ import annotations

import base64
import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt_bytes = os.urandom(16) if salt is None else base64.b64decode(salt.encode("ascii"))
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, 120_000)
    return base64.b64encode(digest).decode("ascii"), base64.b64encode(salt_bytes).decode("ascii")


def verify_password(password: str, password_hash: str, password_salt: str) -> bool:
    candidate, _ = hash_password(password, password_salt)
    return hmac.compare_digest(candidate, password_hash)


def issue_access_token(user_id: str, secret: str, expires_minutes: int = 720) -> tuple[str, datetime]:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": user_id, "exp": expires_at}
    return jwt.encode(payload, secret, algorithm="HS256"), expires_at


def decode_access_token(token: str, secret: str) -> str:
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    subject = payload.get("sub")
    if not subject:
        raise PermissionError("Invalid token payload")
    return str(subject)
