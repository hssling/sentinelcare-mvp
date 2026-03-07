from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

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
SourceMode = Literal["manual_daily_submission", "manual_event_report", "sentinelcare_detected_event", "batch_import", "api_feed"]
EncounterSetting = Literal["emergency", "outpatient", "inpatient", "ICU", "operation_theatre", "labour_room", "day_care"]
ShiftName = Literal["morning", "evening", "night", "unknown"]
CaseStatus = Literal["new", "triaged", "investigating", "actioned", "closed"]
AIProviderName = Literal["openai", "anthropic", "google", "openrouter", "groq", "together", "cohere", "xai"]


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


class EventCase(BaseModel):
    case_id: str
    source_mode: SourceMode
    created_at: datetime
    updated_at: datetime
    facility_id: str
    department_id: str | None = None
    report_id: str | None = None
    event_timestamp: datetime
    encounter_setting: EncounterSetting = "inpatient"
    shift: ShiftName = "unknown"
    patient_age_band: str = "adult"
    patient_sex: str = "unknown"
    special_population_flags: list[str] = Field(default_factory=list)
    encounter_id_local: str | None = None
    high_risk_flag: bool = False
    domain: Domain
    deviation_class: DeviationClass
    process_stage: str
    event_type: str
    actual_harm: str
    potential_harm: str
    severity_level: Severity
    preventability_rating: str = "probable"
    detectability_rating: str = "moderate"
    recurrence_flag: bool = False
    event_summary: str
    what_was_expected: str
    what_happened: str
    immediate_action_taken: str
    evidence_source: str
    linked_system_trace_id: str | None = None
    linked_policy_version: str | None = None
    contributing_factors: list[str] = Field(default_factory=list)
    triage_status: CaseStatus = "new"
    investigation_method: str = "desk review"
    root_cause_category: str | None = None
    corrective_action: str | None = None
    preventive_action: str | None = None
    owner_assigned: str | None = None
    due_date: date | None = None
    closure_status: str = "open"
    closure_date: date | None = None
    closure_quality_rating: str | None = None
    ai_summary: str | None = None
    ai_confidence: float | None = None
    ai_provider: str | None = None
    ai_model: str | None = None
    ai_human_override: str | None = None


class EventCaseCreate(BaseModel):
    source_mode: SourceMode = "manual_event_report"
    department_id: str
    event_timestamp: datetime
    encounter_setting: EncounterSetting
    shift: ShiftName = "unknown"
    patient_age_band: str
    patient_sex: str
    special_population_flags: list[str] = Field(default_factory=list)
    encounter_id_local: str | None = None
    high_risk_flag: bool = False
    domain: Domain
    deviation_class: DeviationClass
    process_stage: str
    event_type: str
    actual_harm: str
    potential_harm: str
    severity_level: Severity
    preventability_rating: str = "probable"
    detectability_rating: str = "moderate"
    recurrence_flag: bool = False
    event_summary: str
    what_was_expected: str
    what_happened: str
    immediate_action_taken: str
    evidence_source: str
    linked_system_trace_id: str | None = None
    linked_policy_version: str | None = None
    contributing_factors: list[str] = Field(default_factory=list)


class EventCaseReviewRequest(BaseModel):
    triage_status: CaseStatus
    owner_assigned: str
    investigation_method: str = "desk review"
    root_cause_category: str | None = None
    corrective_action: str | None = None
    preventive_action: str | None = None
    due_date: date | None = None
    closure_status: str = "open"
    closure_quality_rating: str | None = None
    ai_human_override: str | None = None


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
    admissions: int = 0
    discharges: int = 0
    surgeries: int = 0
    deliveries: int = 0
    critical_results_count: int = 0
    near_misses: int
    no_harm_events: int
    harm_events: int
    severe_events: int
    medication_events: int
    procedure_events: int
    infection_events: int
    diagnostic_events: int
    staffing_shortfall_flag: bool = False
    crowding_flag: bool = False
    system_downtime_flag: bool = False
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
    admissions: int = 0
    discharges: int = 0
    surgeries: int = 0
    deliveries: int = 0
    critical_results_count: int = 0
    near_misses: int
    no_harm_events: int
    harm_events: int
    severe_events: int
    medication_events: int
    procedure_events: int
    infection_events: int
    diagnostic_events: int
    staffing_shortfall_flag: bool = False
    crowding_flag: bool = False
    system_downtime_flag: bool = False
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
    event_cases: int = 0
    sentinel_cases: int = 0


class DomainBreakdownPoint(BaseModel):
    domain: str
    count: int


class TrendSeries(BaseModel):
    scope: str
    points: list[TrendPoint]
    domain_breakdown: list[DomainBreakdownPoint] = Field(default_factory=list)


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
    event_cases_open: int = 0
    learning_actions_due: int = 0
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


class AIProviderCatalogItem(BaseModel):
    provider: AIProviderName
    label: str
    auth_url: str
    docs_url: str
    default_base_url: str
    supported_models: list[str]
    integration_mode: Literal["openai_compatible", "anthropic_messages", "google_generate", "cohere_chat"]


class AIProviderConfigStored(BaseModel):
    config_id: str
    owner_user_id: str
    provider: AIProviderName
    label: str
    model: str
    base_url: str
    api_key_ciphertext: str
    api_key_masked: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class AIProviderConfigView(BaseModel):
    config_id: str
    owner_user_id: str
    provider: AIProviderName
    label: str
    model: str
    base_url: str
    api_key_masked: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class AIProviderConfigCreate(BaseModel):
    provider: AIProviderName
    label: str
    model: str
    api_key: str
    base_url: str | None = None
    is_active: bool = True


class AIAssistRequest(BaseModel):
    case_id: str | None = None
    domain: str | None = None
    severity: str | None = None
    event_summary: str
    what_happened: str = ""
    immediate_action_taken: str = ""
    contributing_factors: list[str] = Field(default_factory=list)


class AIAssistResponse(BaseModel):
    provider: str
    model: str
    summary: str
    confidence: float
    structured_fields: dict[str, Any]


class SurveillanceSnapshot(BaseModel):
    overview: NationalOverview
    facilities: list[Facility]
    reports: list[EventReport]
    signals: list[SafetySignal]
    policies: list[PolicyRecord]
