from __future__ import annotations

from collections import defaultdict
from datetime import timedelta
from typing import Any
from uuid import uuid4

from .agents import (
    agent_catalog,
    build_agent_registry,
)
from .contracts import (
    Alert,
    Event,
    PolicyVersion,
    ProcessingResult,
    QueueItem,
    ReviewAction,
    ValidationReport,
    utcnow,
)
from .engines import (
    CriticalResultClosureEngine,
    DeteriorationSurveillanceEngine,
    MedicationSafetyEngine,
)
from .persistence import SupabaseRepository
from .router import AlertRouter


class SentinelCarePipeline:
    def __init__(self) -> None:
        self.med_engine = MedicationSafetyEngine()
        self.crit_engine = CriticalResultClosureEngine()
        self.det_engine = DeteriorationSurveillanceEngine()
        self.router = AlertRouter()

        self.agents = build_agent_registry()

        self.event_store: list[Event] = []
        self.alert_store: dict[str, Alert] = {}
        self.review_actions: list[ReviewAction] = []
        self.alerts_by_encounter: dict[str, list[str]] = defaultdict(list)
        self.repository = SupabaseRepository.from_env()
        self.execution_log: list[dict[str, Any]] = []
        self.workflow_queue: dict[str, QueueItem] = {}
        self.policies: dict[str, PolicyVersion] = {}
        self.validation_reports: dict[str, ValidationReport] = {}

    def process_event(self, event: Event) -> ProcessingResult:
        tasks = []
        context: dict[str, Any] = {}

        self.event_store.append(event)
        if self.repository:
            self.repository.save_event(event)

        # Stage 1: Foundation agents (A-C)
        for agent_id in ("A", "B", "C"):
            tasks.extend(self.agents[agent_id].run(event, context))

        # Stage 2: Detection engines + agent checks (D-E)
        raw_alerts = (
            self.med_engine.run(event)
            + self.crit_engine.run(event)
            + self.det_engine.run(event)
        )
        context["raw_alerts"] = raw_alerts
        for agent_id in ("D", "E"):
            tasks.extend(self.agents[agent_id].run(event, context))

        routed_alerts: list[Alert] = []
        for alert in raw_alerts:
            routed = self.router.route(alert)
            self.alert_store[routed.alert_id] = routed
            self.alerts_by_encounter[routed.encounter_id].append(routed.alert_id)
            routed_alerts.append(routed)
            queue_item = self._queue_item_from_alert(routed)
            self.workflow_queue[queue_item.queue_id] = queue_item
            if self.repository:
                self.repository.save_alert(routed)
                self.repository.save_queue_item(queue_item)

        # Stage 3-4: Intervention and governance agents (F-H)
        context["routed_alerts"] = routed_alerts
        for agent_id in ("F", "G", "H"):
            tasks.extend(self.agents[agent_id].run(event, context))

        if self.repository:
            for task in tasks:
                self.repository.save_task(task)

        self.execution_log.append(
            {
                "event_id": event.event_id,
                "agent_sequence": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "task_count": len(tasks),
                "alert_count": len(routed_alerts),
            }
        )
        return ProcessingResult(alerts=routed_alerts, tasks=tasks)

    def _queue_item_from_alert(self, alert: Alert) -> QueueItem:
        now = utcnow()
        if alert.severity.value in {"hard-stop proposal", "urgent escalation"}:
            priority = "high"
            due_at = now + timedelta(minutes=15)
            assigned_role = "consultant"
        elif alert.severity.value == "warning":
            priority = "medium"
            due_at = now + timedelta(minutes=60)
            assigned_role = "duty_doctor"
        else:
            priority = "low"
            due_at = now + timedelta(hours=4)
            assigned_role = "bedside_nurse"
        return QueueItem(
            queue_id=str(uuid4()),
            alert_id=alert.alert_id,
            encounter_id=alert.encounter_id,
            patient_id=alert.patient_id,
            priority=priority,
            assigned_role=assigned_role,
            due_at=due_at,
            created_at=now,
            updated_at=now,
        )

    def process_events(self, events: list[Event]) -> ProcessingResult:
        all_alerts: list[Alert] = []
        all_tasks = []
        for event in events:
            result = self.process_event(event)
            all_alerts.extend(result.alerts)
            all_tasks.extend(result.tasks)
        return ProcessingResult(alerts=all_alerts, tasks=all_tasks)

    def record_review_action(
        self,
        alert_id: str,
        acted_by: str,
        action_type: str,
        override_reason: str | None = None,
        comment: str | None = None,
    ) -> ReviewAction:
        action = ReviewAction(
            action_id=str(uuid4()),
            alert_id=alert_id,
            acted_by=acted_by,
            acted_at=utcnow(),
            action_type=action_type,
            override_reason=override_reason,
            comment=comment,
        )
        self.review_actions.append(action)
        if alert_id in self.alert_store:
            self.alert_store[alert_id].status = "closed"
            if self.repository:
                self.repository.save_alert(self.alert_store[alert_id])
        for item in self.workflow_queue.values():
            if item.alert_id == alert_id and item.status != "closed":
                item.status = "closed"
                item.updated_at = utcnow()
                if self.repository:
                    self.repository.save_queue_item(item)
        if self.repository:
            self.repository.save_review_action(action)
        return action

    def list_queue(self, status: str | None = None) -> list[QueueItem]:
        items = list(self.workflow_queue.values())
        if status:
            items = [i for i in items if i.status == status]
        return sorted(items, key=lambda x: x.due_at)

    def escalate_overdue_queue(self) -> dict:
        now = utcnow()
        escalated = 0
        for item in self.workflow_queue.values():
            if item.status == "open" and item.due_at < now:
                item.escalation_level += 1
                item.status = "escalated"
                item.updated_at = now
                escalated += 1
                if self.repository:
                    self.repository.save_queue_item(item)
        return {"escalated_items": escalated, "queue_total": len(self.workflow_queue)}

    def submit_policy(self, policy_name: str, definition: dict[str, Any], submitted_by: str) -> PolicyVersion:
        existing_versions = [
            p for p in self.policies.values() if p.policy_name == policy_name
        ]
        next_version = f"v{len(existing_versions) + 1}"
        policy = PolicyVersion(
            policy_id=str(uuid4()),
            policy_name=policy_name,
            version=next_version,
            status="pending_approval",
            definition=definition,
            submitted_by=submitted_by,
            created_at=utcnow(),
        )
        self.policies[policy.policy_id] = policy
        if self.repository:
            self.repository.save_policy_version(policy)
        return policy

    def approve_policy(self, policy_id: str, approved_by: str) -> PolicyVersion:
        if policy_id not in self.policies:
            raise ValueError(f"Unknown policy id: {policy_id}")
        policy = self.policies[policy_id]
        for other in self.policies.values():
            if other.policy_name == policy.policy_name and other.status == "approved_active":
                other.status = "approved_inactive"
                if self.repository:
                    self.repository.save_policy_version(other)
        policy.status = "approved_active"
        policy.approved_by = approved_by
        policy.approved_at = utcnow()
        if self.repository:
            self.repository.save_policy_version(policy)
        return policy

    def list_policies(self, status: str | None = None) -> list[PolicyVersion]:
        policies = list(self.policies.values())
        if status:
            policies = [p for p in policies if p.status == status]
        return sorted(policies, key=lambda x: x.created_at, reverse=True)

    def generate_validation_report(self, report_type: str = "operational_validation") -> ValidationReport:
        summary = self.summary()
        alerts_total = summary["alerts_total"] or 1
        closed = summary["alerts_by_status"].get("closed", 0)
        urgent = sum(
            1 for alert in self.alert_store.values() if alert.severity.value == "urgent escalation"
        )
        payload = {
            "summary": summary,
            "closure_rate": round(closed / alerts_total, 4),
            "urgent_alerts": urgent,
            "queue_open_items": len([q for q in self.workflow_queue.values() if q.status == "open"]),
            "queue_escalated_items": len([q for q in self.workflow_queue.values() if q.status == "escalated"]),
            "policy_count": len(self.policies),
        }
        report = ValidationReport(
            report_id=str(uuid4()),
            report_type=report_type,
            generated_at=utcnow(),
            payload=payload,
        )
        self.validation_reports[report.report_id] = report
        if self.repository:
            self.repository.save_validation_report(report)
        return report

    def list_validation_reports(self) -> list[ValidationReport]:
        return sorted(self.validation_reports.values(), key=lambda x: x.generated_at, reverse=True)

    def run_single_agent(self, agent_id: str, event: Event) -> dict:
        if agent_id not in self.agents:
            raise ValueError(f"Unknown agent id: {agent_id}")

        context: dict[str, Any] = {}
        raw_alerts = (
            self.med_engine.run(event)
            + self.crit_engine.run(event)
            + self.det_engine.run(event)
        )
        context["raw_alerts"] = raw_alerts
        context["routed_alerts"] = [self.router.route(alert) for alert in raw_alerts]

        tasks = self.agents[agent_id].run(event, context)
        if self.repository:
            for task in tasks:
                self.repository.save_task(task)
        return {
            "agent_id": agent_id,
            "tasks": [t.model_dump(mode="json") for t in tasks],
            "preview_alert_count": len(raw_alerts),
        }

    def run_full_workflow(self, events: list[Event]) -> dict:
        result = self.process_events(events)
        per_agent_task_count: dict[str, int] = defaultdict(int)
        for task in result.tasks:
            agent_code = task.owner_agent.split(" - ")[0]
            per_agent_task_count[agent_code] += 1
        return {
            "events_processed": len(events),
            "alerts_generated": len(result.alerts),
            "tasks_generated": len(result.tasks),
            "per_agent_task_count": dict(sorted(per_agent_task_count.items())),
            "execution_log": self.execution_log[-len(events):],
        }

    def run_capability_demo(self, events: list[Event]) -> dict:
        result = self.process_events(events)
        by_domain: dict[str, int] = defaultdict(int)
        by_severity: dict[str, int] = defaultdict(int)
        by_type: dict[str, int] = defaultdict(int)
        routed_recipients: dict[str, int] = defaultdict(int)

        for alert in result.alerts:
            by_domain[alert.domain] += 1
            by_severity[alert.severity.value] += 1
            by_type[alert.alert_type] += 1
            for recipient in alert.routed_to:
                routed_recipients[recipient] += 1

        # Simulate human handling for urgent and hard-stop alerts.
        auto_closed = 0
        for alert in result.alerts:
            if alert.severity.value in {"urgent escalation", "hard-stop proposal"}:
                self.record_review_action(
                    alert_id=alert.alert_id,
                    acted_by="demo_clinician",
                    action_type="acknowledged_and_actioned",
                    comment="Auto-actioned in capability demo run.",
                )
                auto_closed += 1

        return {
            "events_processed": len(events),
            "alerts_generated": len(result.alerts),
            "tasks_generated": len(result.tasks),
            "alerts_by_domain": dict(sorted(by_domain.items())),
            "alerts_by_severity": dict(sorted(by_severity.items())),
            "top_alert_types": dict(sorted(by_type.items(), key=lambda x: x[1], reverse=True)[:8]),
            "recipient_load": dict(sorted(routed_recipients.items(), key=lambda x: x[1], reverse=True)),
            "auto_review_actions_recorded": auto_closed,
            "post_demo_summary": self.summary(),
        }

    def get_agent_catalog(self) -> list[dict[str, Any]]:
        return agent_catalog(self.agents)

    def summary(self) -> dict:
        by_domain: dict[str, int] = defaultdict(int)
        by_status: dict[str, int] = defaultdict(int)
        for alert in self.alert_store.values():
            by_domain[alert.domain] += 1
            by_status[alert.status] += 1

        return {
            "events_total": len(self.event_store),
            "alerts_total": len(self.alert_store),
            "review_actions_total": len(self.review_actions),
            "agent_catalog_size": len(self.agents),
            "queue_items_total": len(self.workflow_queue),
            "policies_total": len(self.policies),
            "validation_reports_total": len(self.validation_reports),
            "alerts_by_domain": dict(by_domain),
            "alerts_by_status": dict(by_status),
        }
