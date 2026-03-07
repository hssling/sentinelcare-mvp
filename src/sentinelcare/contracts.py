from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Severity(str, Enum):
    INFORMATION = "information"
    RECOMMENDATION = "recommendation"
    PRECAUTION = "precaution"
    WARNING = "warning"
    URGENT_ESCALATION = "urgent escalation"
    HARD_STOP_PROPOSAL = "hard-stop proposal"


class Event(BaseModel):
    event_id: str
    encounter_id: str
    patient_id: str
    event_type: str
    event_time: datetime
    source_system: str = "synthetic"
    payload: dict[str, Any] = Field(default_factory=dict)


class Alert(BaseModel):
    alert_id: str
    encounter_id: str
    patient_id: str
    generated_at: datetime
    domain: str
    alert_type: str
    severity: Severity
    confidence_score: float
    evidence: dict[str, Any]
    recommended_action: dict[str, Any]
    status: str = "open"
    routed_to: list[str] = Field(default_factory=list)


class ReviewAction(BaseModel):
    action_id: str
    alert_id: str
    acted_by: str
    acted_at: datetime
    action_type: str
    override_reason: str | None = None
    comment: str | None = None


class AgentTask(BaseModel):
    task_id: str
    owner_agent: str
    task_name: str
    status: str
    created_at: datetime
    completed_at: datetime | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class ProcessingResult(BaseModel):
    alerts: list[Alert]
    tasks: list[AgentTask]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)

