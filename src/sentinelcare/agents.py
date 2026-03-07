from __future__ import annotations

from typing import Any
from uuid import uuid4

from .contracts import AgentTask, Event, utcnow


class BaseAgent:
    agent_id: str
    name: str
    designated_tasks: tuple[str, ...]

    def _task(self, task_name: str, details: dict[str, Any] | None = None) -> AgentTask:
        now = utcnow()
        return AgentTask(
            task_id=str(uuid4()),
            owner_agent=f"{self.agent_id} - {self.name}",
            task_name=task_name,
            status="completed",
            created_at=now,
            completed_at=now,
            details=details or {},
        )

    def run(self, event: Event, context: dict[str, Any]) -> list[AgentTask]:
        raise NotImplementedError


class FounderProductArchitectAgent(BaseAgent):
    agent_id = "A"
    name = "Founder/Product Architect"
    designated_tasks = ("scope-check", "pilot-domain-priority")

    def run(self, event: Event, context: dict[str, Any]) -> list[AgentTask]:
        return [
            self._task("scope-check", {"event_type": event.event_type}),
            self._task(
                "pilot-domain-priority",
                {"candidate_domains": ["medication_safety", "critical_result_closure", "deterioration_surveillance"]},
            ),
        ]


class ClinicalKnowledgeEngineerAgent(BaseAgent):
    agent_id = "B"
    name = "Clinical Knowledge Engineer"
    designated_tasks = ("rule-context-build", "policy-version-selection")

    def run(self, event: Event, context: dict[str, Any]) -> list[AgentTask]:
        return [
            self._task("rule-context-build", {"encounter_id": event.encounter_id}),
            self._task("policy-version-selection", {"active_policy_version": "v1.0-mvp"}),
        ]


class DataInteroperabilityEngineerAgent(BaseAgent):
    agent_id = "C"
    name = "Data/Interoperability Engineer"
    designated_tasks = ("event-normalization", "terminology-mapping")

    def run(self, event: Event, context: dict[str, Any]) -> list[AgentTask]:
        mapped_keys = sorted(list(event.payload.keys()))[:8]
        return [
            self._task(
                "event-normalization",
                {"source_system": event.source_system, "event_id": event.event_id},
            ),
            self._task("terminology-mapping", {"mapped_payload_keys": mapped_keys}),
        ]


class DetectionMLEngineerAgent(BaseAgent):
    agent_id = "D"
    name = "Detection/ML Engineer"
    designated_tasks = ("detection-run", "risk-score-aggregation")

    def run(self, event: Event, context: dict[str, Any]) -> list[AgentTask]:
        raw_alerts = context.get("raw_alerts", [])
        max_conf = max((a.confidence_score for a in raw_alerts), default=0.0)
        return [
            self._task("detection-run", {"generated_alerts": len(raw_alerts)}),
            self._task("risk-score-aggregation", {"max_confidence": round(max_conf, 4)}),
        ]


class SafetyRedTeamEngineerAgent(BaseAgent):
    agent_id = "E"
    name = "Safety/Red-Team Engineer"
    designated_tasks = ("adversarial-sanity-check", "false-positive-risk-triage")

    def run(self, event: Event, context: dict[str, Any]) -> list[AgentTask]:
        raw_alerts = context.get("raw_alerts", [])
        high_conf = sum(1 for a in raw_alerts if a.confidence_score >= 0.9)
        return [
            self._task("adversarial-sanity-check", {"alerts_checked": len(raw_alerts)}),
            self._task("false-positive-risk-triage", {"high_confidence_alerts": high_conf}),
        ]


class ApplicationEngineerAgent(BaseAgent):
    agent_id = "F"
    name = "Application Engineer"
    designated_tasks = ("route-and-notify", "escalation-path-evaluation")

    def run(self, event: Event, context: dict[str, Any]) -> list[AgentTask]:
        routed_alerts = context.get("routed_alerts", [])
        escalation_recipients = sorted(
            {
                recipient
                for alert in routed_alerts
                for recipient in alert.routed_to
                if recipient in {"consultant", "safety_officer"}
            }
        )
        return [
            self._task("route-and-notify", {"routed_alerts": len(routed_alerts)}),
            self._task("escalation-path-evaluation", {"escalation_recipients": escalation_recipients}),
        ]


class DevSecOpsMLOpsEngineerAgent(BaseAgent):
    agent_id = "G"
    name = "DevSecOps/MLOps Engineer"
    designated_tasks = ("audit-log-write", "release-gate-check")

    def run(self, event: Event, context: dict[str, Any]) -> list[AgentTask]:
        routed_alerts = context.get("routed_alerts", [])
        hard_or_urgent = sum(
            1
            for a in routed_alerts
            if a.severity.value in {"urgent escalation", "hard-stop proposal"}
        )
        return [
            self._task("audit-log-write", {"event_id": event.event_id, "alert_count": len(routed_alerts)}),
            self._task("release-gate-check", {"high_risk_alerts": hard_or_urgent}),
        ]


class ValidationDocumentationEngineerAgent(BaseAgent):
    agent_id = "H"
    name = "Validation/Documentation Engineer"
    designated_tasks = ("validation-record", "quality-report-update")

    def run(self, event: Event, context: dict[str, Any]) -> list[AgentTask]:
        routed_alerts = context.get("routed_alerts", [])
        return [
            self._task(
                "validation-record",
                {"event_type": event.event_type, "alert_count": len(routed_alerts)},
            ),
            self._task("quality-report-update", {"domains": sorted({a.domain for a in routed_alerts})}),
        ]


def build_agent_registry() -> dict[str, BaseAgent]:
    agents: list[BaseAgent] = [
        FounderProductArchitectAgent(),
        ClinicalKnowledgeEngineerAgent(),
        DataInteroperabilityEngineerAgent(),
        DetectionMLEngineerAgent(),
        SafetyRedTeamEngineerAgent(),
        ApplicationEngineerAgent(),
        DevSecOpsMLOpsEngineerAgent(),
        ValidationDocumentationEngineerAgent(),
    ]
    return {a.agent_id: a for a in agents}


def agent_catalog(registry: dict[str, BaseAgent]) -> list[dict[str, Any]]:
    return [
        {
            "agent_id": aid,
            "name": agent.name,
            "designated_tasks": list(agent.designated_tasks),
        }
        for aid, agent in sorted(registry.items())
    ]

