from __future__ import annotations

import os

from .contracts import AgentTask, Alert, Event, ReviewAction

try:
    from supabase import Client, create_client
except ImportError:  # pragma: no cover
    Client = object  # type: ignore[assignment]
    create_client = None  # type: ignore[assignment]


class SupabaseRepository:
    def __init__(self, url: str, service_role_key: str) -> None:
        if create_client is None:
            raise RuntimeError("supabase package not installed")
        self.client: Client = create_client(url, service_role_key)

    @classmethod
    def from_env(cls) -> "SupabaseRepository | None":
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            return None
        return cls(url, key)

    def save_event(self, event: Event) -> None:
        self.client.table("events").insert(
            {
                "event_id": event.event_id,
                "encounter_id": event.encounter_id,
                "patient_id": event.patient_id,
                "event_type": event.event_type,
                "event_time": event.event_time.isoformat(),
                "source_system": event.source_system,
                "payload": event.payload,
            }
        ).execute()

    def save_alert(self, alert: Alert) -> None:
        self.client.table("alerts").upsert(
            {
                "alert_id": alert.alert_id,
                "encounter_id": alert.encounter_id,
                "patient_id": alert.patient_id,
                "domain": alert.domain,
                "alert_type": alert.alert_type,
                "severity": alert.severity.value,
                "confidence_score": alert.confidence_score,
                "evidence": alert.evidence,
                "recommended_action": alert.recommended_action,
                "status": alert.status,
                "routed_to": alert.routed_to,
                "generated_at": alert.generated_at.isoformat(),
            },
            on_conflict="alert_id",
        ).execute()

    def save_task(self, task: AgentTask) -> None:
        self.client.table("agent_tasks").upsert(
            {
                "task_id": task.task_id,
                "owner_agent": task.owner_agent,
                "task_name": task.task_name,
                "status": task.status,
                "details": task.details,
                "created_at": task.created_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            },
            on_conflict="task_id",
        ).execute()

    def save_review_action(self, action: ReviewAction) -> None:
        self.client.table("review_actions").upsert(
            {
                "action_id": action.action_id,
                "alert_id": action.alert_id,
                "acted_by": action.acted_by,
                "acted_at": action.acted_at.isoformat(),
                "action_type": action.action_type,
                "override_reason": action.override_reason,
                "comment": action.comment,
            },
            on_conflict="action_id",
        ).execute()

