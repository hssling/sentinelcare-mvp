from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

Domain = Literal[
    "medication",
    "diagnostic",
    "procedure",
    "deterioration",
    "infection_environment",
    "lab_radiology",
    "care_transition",
    "documentation_communication",
    "device_equipment",
    "operational",
]

DeviationClass = Literal[
    "omission",
    "contradiction",
    "harmful_delay",
    "sequencing_mismatch",
    "closure_failure",
]

Severity = Literal["near_miss", "no_harm", "low", "moderate", "severe", "sentinel"]
ValidationPhase = Literal["design", "retrospective", "silent_mode", "controlled_pilot", "scale_up"]
PolicyState = Literal["draft", "under_review", "approved_pilot", "approved_production", "superseded", "retired"]
RoleName = Literal[
    "facility_reporter",
    "facility_safety_officer",
    "district_reviewer",
    "state_cell_analyst",
    "national_analyst",
    "governance_admin",
]


class Facility(BaseModel):
    facility_id: str
    name: str
    state: str
    district: str
    ownership: Literal["public", "private", "teaching", "trust"]
    level: Literal["medical_college", "district_hospital", "sub_district", "community", "private_hospital"]
    abdm_registry_ready: bool = False
    registry_source: str = "manual"


class Department(BaseModel):
    department_id: str
    facility_id: str
    name: str
    category: Literal["clinical", "support", "quality", "administrative"]
    reporting_enabled: bool = True


class EventReport(BaseModel):
    report_id: str
    event_date: date
    reported_at: datetime
    facility_id: str
    patient_context: str
    domain: Domain
    deviation_class: DeviationClass
    severity: Severity
    process_stage: str
    summary: str
    immediate_action: str
    status: Literal["reported", "triaged", "investigating", "closed"]
    assigned_to: str | None = None
    state_cell: str | None = None
    closure_note: str | None = None


class SafetySignal(BaseModel):
    signal_id: str
    title: str
    scope: Literal["facility", "district", "state", "national"]
    state: str | None = None
    district: str | None = None
    domain: Domain
    deviation_class: DeviationClass
    severity: Severity
    reports_linked: int
    owner_role: str
    next_action: str
    status: Literal["watch", "investigate", "escalated", "closed"]


class PolicyRecord(BaseModel):
    policy_id: str
    title: str
    state: PolicyState
    validation_phase: ValidationPhase
    approver: str
    activation_scope: str
    last_updated: date


class UserIdentity(BaseModel):
    user_id: str
    name: str
    role: RoleName
    state: str | None = None
    district: str | None = None
    facility_id: str | None = None
    department_id: str | None = None
    username: str | None = None
    is_active: bool = True


class UserRecord(UserIdentity):
    password_hash: str
    password_salt: str
    created_at: datetime
    created_by: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class SessionToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserIdentity


class DailySurveillanceSubmission(BaseModel):
    submission_id: str
    submission_date: date
    facility_id: str
    department_id: str
    submitted_by: str
    patient_days: int
    near_misses: int
    no_harm_events: int
    harm_events: int
    severe_events: int
    medication_events: int
    procedure_events: int
    infection_events: int
    diagnostic_events: int
    escalation_required: bool = False
    notes: str = ""
    reviewed_by: str | None = None
    review_status: Literal["submitted", "reviewed", "actioned"] = "submitted"
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DailySubmissionCreate(BaseModel):
    submission_date: date
    department_id: str
    patient_days: int
    near_misses: int
    no_harm_events: int
    harm_events: int
    severe_events: int
    medication_events: int
    procedure_events: int
    infection_events: int
    diagnostic_events: int
    escalation_required: bool = False
    notes: str = ""


class SubmissionReviewRequest(BaseModel):
    review_status: Literal["reviewed", "actioned"]
    reviewed_by: str
    notes: str = ""


class UserCreateRequest(BaseModel):
    name: str
    username: str
    password: str
    role: RoleName
    state: str | None = None
    district: str | None = None
    facility_id: str | None = None
    department_id: str | None = None


class NotificationRecord(BaseModel):
    notification_id: str
    created_at: datetime
    user_id: str | None = None
    scope: Literal["facility", "state", "national"]
    title: str
    message: str
    severity: Severity
    status: Literal["open", "acknowledged", "closed"] = "open"
    facility_id: str | None = None
    state: str | None = None
    entity_type: str | None = None
    entity_id: str | None = None


class NotificationAcknowledgeRequest(BaseModel):
    status: Literal["acknowledged", "closed"]


class AuditLogRecord(BaseModel):
    audit_id: str
    created_at: datetime
    actor_user_id: str | None = None
    action: str
    entity_type: str
    entity_id: str
    detail: str


class TrendPoint(BaseModel):
    date: date
    patient_days: int
    near_misses: int
    harm_events: int
    severe_events: int


class TrendSeries(BaseModel):
    scope: str
    points: list[TrendPoint]


class DashboardIndicator(BaseModel):
    label: str
    value: int
    trend: str


class DashboardAlert(BaseModel):
    alert_id: str
    severity: Severity
    title: str
    detail: str
    owner_role: str


class DashboardSnapshot(BaseModel):
    scope: str
    indicators: list[DashboardIndicator]
    alerts: list[DashboardAlert]
    submissions_pending_review: int
    reports_open: int
    trend: TrendSeries | None = None


class FacilityImportRecord(BaseModel):
    facility_id: str
    name: str
    state: str
    district: str
    ownership: Literal["public", "private", "teaching", "trust"]
    level: Literal["medical_college", "district_hospital", "sub_district", "community", "private_hospital"]
    abdm_registry_ready: bool = False
    registry_source: str = "csv_import"


class PilotStateCell(BaseModel):
    state_cell_id: str
    state: str
    nodal_unit: str
    lead_name: str
    status: Literal["design", "pilot", "active"]
    facilities_mapped: int


class TriageRequest(BaseModel):
    status: Literal["triaged", "investigating"]
    assigned_to: str
    state_cell: str


class ClosureRequest(BaseModel):
    closure_note: str


class RegistryImportRequest(BaseModel):
    imported_by: str
    facilities: list[FacilityImportRecord]


class TraceStep(BaseModel):
    step: str
    finding: str
    output: str


class EventTrace(BaseModel):
    report_id: str
    facility: str
    state: str
    district: str
    domain: Domain
    deviation_class: DeviationClass
    severity: Severity
    validation_phase: ValidationPhase
    active_policy_version: str
    trace_steps: list[TraceStep]
    routed_to: str
    closure_requirement: str


class NationalOverview(BaseModel):
    reporting_period: str
    facilities_onboarded: int
    states_covered: int
    reports_received: int
    open_investigations: int
    escalated_signals: int
    sentinel_events: int
    validation_phase: ValidationPhase


class IntegrationProfile(BaseModel):
    target_systems: list[str]
    input_modes: list[str]
    standards: list[str]
    privacy_controls: list[str]
    deployment_model: str = Field(default="federated")


class SurveillanceSnapshot(BaseModel):
    overview: NationalOverview
    facilities: list[Facility]
    reports: list[EventReport]
    signals: list[SafetySignal]
    policies: list[PolicyRecord]
