from __future__ import annotations

from uuid import uuid4

from .contracts import AgentTask, Alert, Event, utcnow


class BaseAgent:
    name: str

    def task(self, task_name: str, details: dict | None = None) -> AgentTask:
        now = utcnow()
        return AgentTask(
            task_id=str(uuid4()),
            owner_agent=self.name,
            task_name=task_name,
            status="completed",
            created_at=now,
            completed_at=now,
            details=details or {},
        )


class FounderProductArchitectAgent(BaseAgent):
    name = "Agent A - Founder/Product Architect"

    def scope_task(self, event: Event) -> AgentTask:
        return self.task("scope-check", {"event_type": event.event_type})


class ClinicalKnowledgeEngineerAgent(BaseAgent):
    name = "Agent B - Clinical Knowledge Engineer"

    def rule_context_task(self, event: Event) -> AgentTask:
        return self.task("rule-context-build", {"encounter_id": event.encounter_id})


class DataInteroperabilityEngineerAgent(BaseAgent):
    name = "Agent C - Data/Interoperability Engineer"

    def normalization_task(self, event: Event) -> AgentTask:
        return self.task(
            "event-normalization",
            {"source_system": event.source_system, "event_id": event.event_id},
        )


class DetectionMLEngineerAgent(BaseAgent):
    name = "Agent D - Detection/ML Engineer"

    def detection_task(self, alert_count: int) -> AgentTask:
        return self.task("detection-run", {"generated_alerts": alert_count})


class SafetyRedTeamEngineerAgent(BaseAgent):
    name = "Agent E - Safety/Red-Team Engineer"

    def challenge_task(self, alerts: list[Alert]) -> AgentTask:
        return self.task("adversarial-sanity-check", {"alerts_checked": len(alerts)})


class ApplicationEngineerAgent(BaseAgent):
    name = "Agent F - Application Engineer"

    def routing_task(self, route_count: int) -> AgentTask:
        return self.task("route-and-notify", {"routed_alerts": route_count})


class DevSecOpsMLOpsEngineerAgent(BaseAgent):
    name = "Agent G - DevSecOps/MLOps Engineer"

    def audit_task(self, event: Event, alert_count: int) -> AgentTask:
        return self.task(
            "audit-log-write",
            {"event_id": event.event_id, "alert_count": alert_count},
        )


class ValidationDocumentationEngineerAgent(BaseAgent):
    name = "Agent H - Validation/Documentation Engineer"

    def validation_task(self, event: Event, alert_count: int) -> AgentTask:
        return self.task(
            "validation-record",
            {"event_type": event.event_type, "alert_count": alert_count},
        )

