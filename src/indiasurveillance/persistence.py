from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import date, datetime, timezone
from typing import Any

from supabase import Client, create_client

from .contracts import (
    AIProviderConfigStored,
    AuditLogRecord,
    DailySurveillanceSubmission,
    Department,
    DomainBreakdownPoint,
    EventCase,
    EventReport,
    Facility,
    NotificationRecord,
    PilotStateCell,
    PolicyRecord,
    SafetySignal,
    TrendPoint,
    UserRecord,
)
from .demo_data import (
    build_demo_daily_submissions,
    build_demo_departments,
    build_demo_event_cases,
    build_demo_snapshot,
    build_demo_state_cells,
    build_demo_users,
)
from .security import hash_password


def _iso_date(value: date | datetime | str | None) -> date | None:
    if value is None or isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    return date.fromisoformat(value)


def _iso_datetime(value: datetime | str | None) -> datetime | None:
    if value is None or isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _serialize(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump(mode="json")
    raise TypeError("Unsupported model")


def _clamp_non_negative(value: int) -> int:
    return max(0, value)


class StorageBackend(ABC):
    @abstractmethod
    def bootstrap_if_empty(self) -> None: ...

    @abstractmethod
    def list_facilities(self) -> list[Facility]: ...

    @abstractmethod
    def list_reports(self) -> list[EventReport]: ...

    @abstractmethod
    def list_event_cases(self) -> list[EventCase]: ...

    @abstractmethod
    def create_event_case(self, event_case: EventCase) -> EventCase: ...

    @abstractmethod
    def update_event_case(self, event_case: EventCase) -> EventCase: ...

    @abstractmethod
    def get_event_case(self, case_id: str) -> EventCase | None: ...

    @abstractmethod
    def list_signals(self) -> list[SafetySignal]: ...

    @abstractmethod
    def list_policies(self) -> list[PolicyRecord]: ...

    @abstractmethod
    def list_users(self) -> list[UserRecord]: ...

    @abstractmethod
    def get_user(self, user_id: str) -> UserRecord | None: ...

    @abstractmethod
    def get_user_by_username(self, username: str) -> UserRecord | None: ...

    @abstractmethod
    def create_user(self, user: UserRecord) -> UserRecord: ...

    @abstractmethod
    def list_state_cells(self) -> list[PilotStateCell]: ...

    @abstractmethod
    def list_departments(self, facility_id: str | None = None) -> list[Department]: ...

    @abstractmethod
    def list_daily_submissions(self) -> list[DailySurveillanceSubmission]: ...

    @abstractmethod
    def create_daily_submission(self, submission: DailySurveillanceSubmission) -> DailySurveillanceSubmission: ...

    @abstractmethod
    def update_daily_submission(self, submission: DailySurveillanceSubmission) -> DailySurveillanceSubmission: ...

    @abstractmethod
    def import_facility(self, facility: Facility) -> Facility: ...

    @abstractmethod
    def get_report(self, report_id: str) -> EventReport | None: ...

    @abstractmethod
    def update_report(self, report: EventReport) -> EventReport: ...

    @abstractmethod
    def create_notification(self, notification: NotificationRecord) -> NotificationRecord: ...

    @abstractmethod
    def list_notifications(self, user_id: str | None = None) -> list[NotificationRecord]: ...

    @abstractmethod
    def update_notification(self, notification: NotificationRecord) -> NotificationRecord: ...

    @abstractmethod
    def create_audit_log(self, audit: AuditLogRecord) -> AuditLogRecord: ...

    @abstractmethod
    def list_audit_logs(self, limit: int = 50) -> list[AuditLogRecord]: ...

    @abstractmethod
    def trend_points(self, facility_id: str | None = None, state: str | None = None) -> list[TrendPoint]: ...

    @abstractmethod
    def domain_breakdown(self, facility_id: str | None = None, state: str | None = None) -> list[DomainBreakdownPoint]: ...

    @abstractmethod
    def list_ai_provider_configs(self, owner_user_id: str) -> list[AIProviderConfigStored]: ...

    @abstractmethod
    def upsert_ai_provider_config(self, config: AIProviderConfigStored) -> AIProviderConfigStored: ...

    @abstractmethod
    def get_ai_provider_config(self, owner_user_id: str, config_id: str) -> AIProviderConfigStored | None: ...

    @abstractmethod
    def get_active_ai_provider_config(self, owner_user_id: str) -> AIProviderConfigStored | None: ...


class InMemoryStorage(StorageBackend):
    def __init__(self) -> None:
        snapshot = build_demo_snapshot()
        now = datetime(2026, 3, 8, 9, 0, 0, tzinfo=timezone.utc)
        self.facilities = {item.facility_id: item for item in snapshot.facilities}
        self.reports = {item.report_id: item for item in snapshot.reports}
        self.event_cases = {item.case_id: item for item in build_demo_event_cases()}
        self.signals = {item.signal_id: item for item in snapshot.signals}
        self.policies = {item.policy_id: item for item in snapshot.policies}
        self.departments = {item.department_id: item for item in build_demo_departments()}
        self.state_cells = {item.state_cell_id: item for item in build_demo_state_cells()}
        self.daily_submissions = {item.submission_id: item for item in build_demo_daily_submissions()}
        self.notifications: dict[str, NotificationRecord] = {}
        self.audit_logs: dict[str, AuditLogRecord] = {}
        self.users: dict[str, UserRecord] = {}
        self.ai_provider_configs: dict[str, AIProviderConfigStored] = {}
        for user in build_demo_users():
            password_hash, password_salt = hash_password("pass123")
            self.users[user.user_id] = UserRecord(
                **user.model_dump(),
                password_hash=password_hash,
                password_salt=password_salt,
                created_at=now,
                created_by="seed",
            )

    def bootstrap_if_empty(self) -> None:
        return None

    def list_facilities(self) -> list[Facility]:
        return list(self.facilities.values())

    def list_reports(self) -> list[EventReport]:
        return list(self.reports.values())

    def list_event_cases(self) -> list[EventCase]:
        return list(self.event_cases.values())

    def create_event_case(self, event_case: EventCase) -> EventCase:
        self.event_cases[event_case.case_id] = event_case
        return event_case

    def update_event_case(self, event_case: EventCase) -> EventCase:
        self.event_cases[event_case.case_id] = event_case
        return event_case

    def get_event_case(self, case_id: str) -> EventCase | None:
        return self.event_cases.get(case_id)

    def list_signals(self) -> list[SafetySignal]:
        return list(self.signals.values())

    def list_policies(self) -> list[PolicyRecord]:
        return list(self.policies.values())

    def list_users(self) -> list[UserRecord]:
        return list(self.users.values())

    def get_user(self, user_id: str) -> UserRecord | None:
        return self.users.get(user_id)

    def get_user_by_username(self, username: str) -> UserRecord | None:
        return next((item for item in self.users.values() if item.username == username), None)

    def create_user(self, user: UserRecord) -> UserRecord:
        self.users[user.user_id] = user
        return user

    def list_state_cells(self) -> list[PilotStateCell]:
        return list(self.state_cells.values())

    def list_departments(self, facility_id: str | None = None) -> list[Department]:
        items = list(self.departments.values())
        return [item for item in items if not facility_id or item.facility_id == facility_id]

    def list_daily_submissions(self) -> list[DailySurveillanceSubmission]:
        return list(self.daily_submissions.values())

    def create_daily_submission(self, submission: DailySurveillanceSubmission) -> DailySurveillanceSubmission:
        self.daily_submissions[submission.submission_id] = submission
        return submission

    def update_daily_submission(self, submission: DailySurveillanceSubmission) -> DailySurveillanceSubmission:
        self.daily_submissions[submission.submission_id] = submission
        return submission

    def import_facility(self, facility: Facility) -> Facility:
        self.facilities[facility.facility_id] = facility
        return facility

    def get_report(self, report_id: str) -> EventReport | None:
        return self.reports.get(report_id)

    def update_report(self, report: EventReport) -> EventReport:
        self.reports[report.report_id] = report
        return report

    def create_notification(self, notification: NotificationRecord) -> NotificationRecord:
        self.notifications[notification.notification_id] = notification
        return notification

    def list_notifications(self, user_id: str | None = None) -> list[NotificationRecord]:
        items = list(self.notifications.values())
        return [item for item in items if not user_id or item.user_id == user_id or item.user_id is None]

    def update_notification(self, notification: NotificationRecord) -> NotificationRecord:
        self.notifications[notification.notification_id] = notification
        return notification

    def create_audit_log(self, audit: AuditLogRecord) -> AuditLogRecord:
        self.audit_logs[audit.audit_id] = audit
        return audit

    def list_audit_logs(self, limit: int = 50) -> list[AuditLogRecord]:
        items = sorted(self.audit_logs.values(), key=lambda item: item.created_at, reverse=True)
        return items[:limit]

    def trend_points(self, facility_id: str | None = None, state: str | None = None) -> list[TrendPoint]:
        submissions = self.list_daily_submissions()
        cases = self.list_event_cases()
        if facility_id:
            submissions = [item for item in submissions if item.facility_id == facility_id]
            cases = [item for item in cases if item.facility_id == facility_id]
        if state:
            facility_ids = {item.facility_id for item in self.list_facilities() if item.state == state}
            submissions = [item for item in submissions if item.facility_id in facility_ids]
            cases = [item for item in cases if item.facility_id in facility_ids]
        buckets: dict[date, dict[str, int]] = defaultdict(
            lambda: {"patient_days": 0, "near_misses": 0, "harm_events": 0, "severe_events": 0, "event_cases": 0, "sentinel_cases": 0}
        )
        for item in submissions:
            bucket = buckets[item.submission_date]
            bucket["patient_days"] += _clamp_non_negative(item.patient_days)
            bucket["near_misses"] += _clamp_non_negative(item.near_misses)
            bucket["harm_events"] += _clamp_non_negative(item.harm_events)
            bucket["severe_events"] += _clamp_non_negative(item.severe_events)
        for item in cases:
            bucket = buckets[item.event_timestamp.date()]
            bucket["event_cases"] += 1
            if item.severity_level == "sentinel":
                bucket["sentinel_cases"] += 1
        return [TrendPoint(date=key, **value) for key, value in sorted(buckets.items())]

    def domain_breakdown(self, facility_id: str | None = None, state: str | None = None) -> list[DomainBreakdownPoint]:
        cases = self.list_event_cases()
        if facility_id:
            cases = [item for item in cases if item.facility_id == facility_id]
        if state:
            facility_ids = {item.facility_id for item in self.list_facilities() if item.state == state}
            cases = [item for item in cases if item.facility_id in facility_ids]
        counts: dict[str, int] = defaultdict(int)
        for item in cases:
            counts[item.domain] += 1
        return [DomainBreakdownPoint(domain=key, count=value) for key, value in sorted(counts.items())]

    def list_ai_provider_configs(self, owner_user_id: str) -> list[AIProviderConfigStored]:
        return [item for item in self.ai_provider_configs.values() if item.owner_user_id == owner_user_id]

    def upsert_ai_provider_config(self, config: AIProviderConfigStored) -> AIProviderConfigStored:
        if config.is_active:
            for existing in self.ai_provider_configs.values():
                if existing.owner_user_id == config.owner_user_id:
                    existing.is_active = existing.config_id == config.config_id
        self.ai_provider_configs[config.config_id] = config
        return config

    def get_ai_provider_config(self, owner_user_id: str, config_id: str) -> AIProviderConfigStored | None:
        config = self.ai_provider_configs.get(config_id)
        if config and config.owner_user_id == owner_user_id:
            return config
        return None

    def get_active_ai_provider_config(self, owner_user_id: str) -> AIProviderConfigStored | None:
        return next((item for item in self.ai_provider_configs.values() if item.owner_user_id == owner_user_id and item.is_active), None)


class SupabaseStorage(StorageBackend):
    def __init__(self, url: str, service_role_key: str) -> None:
        self.client: Client = create_client(url, service_role_key)

    def bootstrap_if_empty(self) -> None:
        memory = InMemoryStorage()
        if self._table_empty("facilities", "facility_id"):
            for facility in memory.list_facilities():
                self.import_facility(facility)
        if self._table_empty("departments", "department_id"):
            for department in memory.list_departments():
                self.client.table("departments").upsert(_serialize(department)).execute()
        if self._table_empty("state_cells", "state_cell_id"):
            for state_cell in memory.list_state_cells():
                self.client.table("state_cells").upsert(_serialize(state_cell)).execute()
        if self._table_empty("policies", "policy_id"):
            for policy in memory.list_policies():
                self.client.table("policies").upsert(_serialize(policy)).execute()
        if self._table_empty("event_reports", "report_id"):
            for report in memory.list_reports():
                self.client.table("event_reports").upsert(_serialize(report)).execute()
        if self._table_empty("event_cases", "case_id"):
            for event_case in memory.list_event_cases():
                self.client.table("event_cases").upsert(_serialize(event_case)).execute()
        if self._table_empty("safety_signals", "signal_id"):
            for signal in memory.list_signals():
                self.client.table("safety_signals").upsert(_serialize(signal)).execute()
        if self._table_empty("daily_submissions", "submission_id"):
            for submission in memory.list_daily_submissions():
                self.client.table("daily_submissions").upsert(_serialize(submission)).execute()
        if self._table_empty("surveillance_users", "user_id"):
            for user in memory.list_users():
                self.create_user(user)

    def _table_empty(self, table: str, key: str) -> bool:
        try:
            existing = self.client.table(table).select(key, count="exact").limit(1).execute()
        except Exception:
            return True
        return not getattr(existing, "count", 0)

    def _rows(self, table: str, order: str | None = None, desc: bool = False) -> list[dict[str, Any]]:
        query = self.client.table(table).select("*")
        if order:
            query = query.order(order, desc=desc)
        response = query.execute()
        return list(response.data or [])

    def list_facilities(self) -> list[Facility]:
        return [Facility(**row) for row in self._rows("facilities", "facility_id")]

    def list_reports(self) -> list[EventReport]:
        rows = self._rows("event_reports", "reported_at")
        for row in rows:
            row["event_date"] = _iso_date(row.get("event_date"))
            row["reported_at"] = _iso_datetime(row.get("reported_at"))
        return [EventReport(**row) for row in rows]

    def list_event_cases(self) -> list[EventCase]:
        try:
            rows = self._rows("event_cases", "event_timestamp", desc=True)
        except Exception:
            return []
        for row in rows:
            row["created_at"] = _iso_datetime(row.get("created_at"))
            row["updated_at"] = _iso_datetime(row.get("updated_at"))
            row["event_timestamp"] = _iso_datetime(row.get("event_timestamp"))
            row["due_date"] = _iso_date(row.get("due_date"))
            row["closure_date"] = _iso_date(row.get("closure_date"))
        return [EventCase(**row) for row in rows]

    def create_event_case(self, event_case: EventCase) -> EventCase:
        self.client.table("event_cases").insert(_serialize(event_case)).execute()
        return event_case

    def update_event_case(self, event_case: EventCase) -> EventCase:
        payload = _serialize(event_case)
        payload["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.client.table("event_cases").update(payload).eq("case_id", event_case.case_id).execute()
        return event_case

    def get_event_case(self, case_id: str) -> EventCase | None:
        try:
            response = self.client.table("event_cases").select("*").eq("case_id", case_id).limit(1).execute()
        except Exception:
            return None
        if not response.data:
            return None
        row = dict(response.data[0])
        row["created_at"] = _iso_datetime(row.get("created_at"))
        row["updated_at"] = _iso_datetime(row.get("updated_at"))
        row["event_timestamp"] = _iso_datetime(row.get("event_timestamp"))
        row["due_date"] = _iso_date(row.get("due_date"))
        row["closure_date"] = _iso_date(row.get("closure_date"))
        return EventCase(**row)

    def list_signals(self) -> list[SafetySignal]:
        return [SafetySignal(**row) for row in self._rows("safety_signals", "signal_id")]

    def list_policies(self) -> list[PolicyRecord]:
        rows = self._rows("policies", "policy_id")
        for row in rows:
            row["last_updated"] = _iso_date(row.get("last_updated"))
        return [PolicyRecord(**row) for row in rows]

    def list_users(self) -> list[UserRecord]:
        rows = self._rows("surveillance_users", "username")
        for row in rows:
            row["created_at"] = _iso_datetime(row.get("created_at"))
        return [UserRecord(**row) for row in rows]

    def get_user(self, user_id: str) -> UserRecord | None:
        response = self.client.table("surveillance_users").select("*").eq("user_id", user_id).limit(1).execute()
        if not response.data:
            return None
        row = dict(response.data[0])
        row["created_at"] = _iso_datetime(row.get("created_at"))
        return UserRecord(**row)

    def get_user_by_username(self, username: str) -> UserRecord | None:
        response = self.client.table("surveillance_users").select("*").eq("username", username).limit(1).execute()
        if not response.data:
            return None
        row = dict(response.data[0])
        row["created_at"] = _iso_datetime(row.get("created_at"))
        return UserRecord(**row)

    def create_user(self, user: UserRecord) -> UserRecord:
        self.client.table("surveillance_users").upsert(_serialize(user)).execute()
        return user

    def list_state_cells(self) -> list[PilotStateCell]:
        return [PilotStateCell(**row) for row in self._rows("state_cells", "state")]

    def list_departments(self, facility_id: str | None = None) -> list[Department]:
        query = self.client.table("departments").select("*")
        if facility_id:
            query = query.eq("facility_id", facility_id)
        response = query.order("department_id").execute()
        return [Department(**row) for row in response.data or []]

    def list_daily_submissions(self) -> list[DailySurveillanceSubmission]:
        rows = self._rows("daily_submissions", "submission_date", desc=True)
        for row in rows:
            row["submission_date"] = _iso_date(row.get("submission_date"))
            row["created_at"] = _iso_datetime(row.get("created_at"))
            row["updated_at"] = _iso_datetime(row.get("updated_at"))
        return [DailySurveillanceSubmission(**row) for row in rows]

    def create_daily_submission(self, submission: DailySurveillanceSubmission) -> DailySurveillanceSubmission:
        self.client.table("daily_submissions").insert(_serialize(submission)).execute()
        return submission

    def update_daily_submission(self, submission: DailySurveillanceSubmission) -> DailySurveillanceSubmission:
        payload = _serialize(submission)
        payload["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.client.table("daily_submissions").update(payload).eq("submission_id", submission.submission_id).execute()
        return submission

    def import_facility(self, facility: Facility) -> Facility:
        self.client.table("facilities").upsert(_serialize(facility)).execute()
        return facility

    def get_report(self, report_id: str) -> EventReport | None:
        response = self.client.table("event_reports").select("*").eq("report_id", report_id).limit(1).execute()
        if not response.data:
            return None
        row = dict(response.data[0])
        row["event_date"] = _iso_date(row.get("event_date"))
        row["reported_at"] = _iso_datetime(row.get("reported_at"))
        return EventReport(**row)

    def update_report(self, report: EventReport) -> EventReport:
        self.client.table("event_reports").update(_serialize(report)).eq("report_id", report.report_id).execute()
        return report

    def create_notification(self, notification: NotificationRecord) -> NotificationRecord:
        self.client.table("notifications").insert(_serialize(notification)).execute()
        return notification

    def list_notifications(self, user_id: str | None = None) -> list[NotificationRecord]:
        query = self.client.table("notifications").select("*")
        if user_id:
            query = query.or_(f"user_id.eq.{user_id},user_id.is.null")
        response = query.order("created_at", desc=True).execute()
        rows = list(response.data or [])
        for row in rows:
            row["created_at"] = _iso_datetime(row.get("created_at"))
        return [NotificationRecord(**row) for row in rows]

    def update_notification(self, notification: NotificationRecord) -> NotificationRecord:
        self.client.table("notifications").update(_serialize(notification)).eq("notification_id", notification.notification_id).execute()
        return notification

    def create_audit_log(self, audit: AuditLogRecord) -> AuditLogRecord:
        self.client.table("audit_logs").insert(_serialize(audit)).execute()
        return audit

    def list_audit_logs(self, limit: int = 50) -> list[AuditLogRecord]:
        response = self.client.table("audit_logs").select("*").order("created_at", desc=True).limit(limit).execute()
        rows = list(response.data or [])
        for row in rows:
            row["created_at"] = _iso_datetime(row.get("created_at"))
        return [AuditLogRecord(**row) for row in rows]

    def trend_points(self, facility_id: str | None = None, state: str | None = None) -> list[TrendPoint]:
        submissions = self.list_daily_submissions()
        cases = self.list_event_cases()
        if facility_id:
            submissions = [item for item in submissions if item.facility_id == facility_id]
            cases = [item for item in cases if item.facility_id == facility_id]
        if state:
            facility_ids = {item.facility_id for item in self.list_facilities() if item.state == state}
            submissions = [item for item in submissions if item.facility_id in facility_ids]
            cases = [item for item in cases if item.facility_id in facility_ids]
        buckets: dict[date, dict[str, int]] = defaultdict(
            lambda: {"patient_days": 0, "near_misses": 0, "harm_events": 0, "severe_events": 0, "event_cases": 0, "sentinel_cases": 0}
        )
        for item in submissions:
            bucket = buckets[item.submission_date]
            bucket["patient_days"] += _clamp_non_negative(item.patient_days)
            bucket["near_misses"] += _clamp_non_negative(item.near_misses)
            bucket["harm_events"] += _clamp_non_negative(item.harm_events)
            bucket["severe_events"] += _clamp_non_negative(item.severe_events)
        for item in cases:
            bucket = buckets[item.event_timestamp.date()]
            bucket["event_cases"] += 1
            if item.severity_level == "sentinel":
                bucket["sentinel_cases"] += 1
        return [TrendPoint(date=key, **value) for key, value in sorted(buckets.items())]

    def domain_breakdown(self, facility_id: str | None = None, state: str | None = None) -> list[DomainBreakdownPoint]:
        cases = self.list_event_cases()
        if facility_id:
            cases = [item for item in cases if item.facility_id == facility_id]
        if state:
            facility_ids = {item.facility_id for item in self.list_facilities() if item.state == state}
            cases = [item for item in cases if item.facility_id in facility_ids]
        counts: dict[str, int] = defaultdict(int)
        for item in cases:
            counts[item.domain] += 1
        return [DomainBreakdownPoint(domain=key, count=value) for key, value in sorted(counts.items())]

    def list_ai_provider_configs(self, owner_user_id: str) -> list[AIProviderConfigStored]:
        try:
            response = self.client.table("ai_provider_configs").select("*").eq("owner_user_id", owner_user_id).order("updated_at", desc=True).execute()
        except Exception:
            return []
        rows = list(response.data or [])
        for row in rows:
            row["created_at"] = _iso_datetime(row.get("created_at"))
            row["updated_at"] = _iso_datetime(row.get("updated_at"))
        return [AIProviderConfigStored(**row) for row in rows]

    def upsert_ai_provider_config(self, config: AIProviderConfigStored) -> AIProviderConfigStored:
        if config.is_active:
            try:
                self.client.table("ai_provider_configs").update({"is_active": False}).eq("owner_user_id", config.owner_user_id).execute()
            except Exception:
                pass
        self.client.table("ai_provider_configs").upsert(_serialize(config)).execute()
        return config

    def get_ai_provider_config(self, owner_user_id: str, config_id: str) -> AIProviderConfigStored | None:
        try:
            response = self.client.table("ai_provider_configs").select("*").eq("owner_user_id", owner_user_id).eq("config_id", config_id).limit(1).execute()
        except Exception:
            return None
        if not response.data:
            return None
        row = dict(response.data[0])
        row["created_at"] = _iso_datetime(row.get("created_at"))
        row["updated_at"] = _iso_datetime(row.get("updated_at"))
        return AIProviderConfigStored(**row)

    def get_active_ai_provider_config(self, owner_user_id: str) -> AIProviderConfigStored | None:
        try:
            response = self.client.table("ai_provider_configs").select("*").eq("owner_user_id", owner_user_id).eq("is_active", True).limit(1).execute()
        except Exception:
            return None
        if not response.data:
            return None
        row = dict(response.data[0])
        row["created_at"] = _iso_datetime(row.get("created_at"))
        row["updated_at"] = _iso_datetime(row.get("updated_at"))
        return AIProviderConfigStored(**row)
