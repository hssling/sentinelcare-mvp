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


class Facility(BaseModel):
    facility_id: str
    name: str
    state: str
    district: str
    ownership: Literal["public", "private", "teaching", "trust"]
    level: Literal["medical_college", "district_hospital", "sub_district", "community", "private_hospital"]
    abdm_registry_ready: bool = False
    registry_source: str = "manual"


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
    role: Literal[
        "facility_reporter",
        "facility_safety_officer",
        "district_reviewer",
        "state_cell_analyst",
        "national_analyst",
        "governance_admin",
    ]
    state: str | None = None
    district: str | None = None
    facility_id: str | None = None


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
