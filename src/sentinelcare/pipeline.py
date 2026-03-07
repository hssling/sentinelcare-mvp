from __future__ import annotations

from collections import defaultdict
from uuid import uuid4

from .agents import (
    ApplicationEngineerAgent,
    ClinicalKnowledgeEngineerAgent,
    DataInteroperabilityEngineerAgent,
    DetectionMLEngineerAgent,
    DevSecOpsMLOpsEngineerAgent,
    FounderProductArchitectAgent,
    SafetyRedTeamEngineerAgent,
    ValidationDocumentationEngineerAgent,
)
from .contracts import Alert, Event, ProcessingResult, ReviewAction, utcnow
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

        self.agent_a = FounderProductArchitectAgent()
        self.agent_b = ClinicalKnowledgeEngineerAgent()
        self.agent_c = DataInteroperabilityEngineerAgent()
        self.agent_d = DetectionMLEngineerAgent()
        self.agent_e = SafetyRedTeamEngineerAgent()
        self.agent_f = ApplicationEngineerAgent()
        self.agent_g = DevSecOpsMLOpsEngineerAgent()
        self.agent_h = ValidationDocumentationEngineerAgent()

        self.event_store: list[Event] = []
        self.alert_store: dict[str, Alert] = {}
        self.review_actions: list[ReviewAction] = []
        self.alerts_by_encounter: dict[str, list[str]] = defaultdict(list)
        self.repository = SupabaseRepository.from_env()

    def process_event(self, event: Event) -> ProcessingResult:
        tasks = [
            self.agent_a.scope_task(event),
            self.agent_b.rule_context_task(event),
            self.agent_c.normalization_task(event),
        ]

        self.event_store.append(event)
        if self.repository:
            self.repository.save_event(event)
        raw_alerts = (
            self.med_engine.run(event)
            + self.crit_engine.run(event)
            + self.det_engine.run(event)
        )
        tasks.append(self.agent_d.detection_task(len(raw_alerts)))
        tasks.append(self.agent_e.challenge_task(raw_alerts))

        routed_alerts: list[Alert] = []
        for alert in raw_alerts:
            routed = self.router.route(alert)
            self.alert_store[routed.alert_id] = routed
            self.alerts_by_encounter[routed.encounter_id].append(routed.alert_id)
            routed_alerts.append(routed)
            if self.repository:
                self.repository.save_alert(routed)

        tasks.append(self.agent_f.routing_task(len(routed_alerts)))
        tasks.append(self.agent_g.audit_task(event, len(routed_alerts)))
        tasks.append(self.agent_h.validation_task(event, len(routed_alerts)))
        if self.repository:
            for task in tasks:
                self.repository.save_task(task)

        return ProcessingResult(alerts=routed_alerts, tasks=tasks)

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
        if self.repository:
            self.repository.save_review_action(action)
        return action

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
            "alerts_by_domain": dict(by_domain),
            "alerts_by_status": dict(by_status),
        }
