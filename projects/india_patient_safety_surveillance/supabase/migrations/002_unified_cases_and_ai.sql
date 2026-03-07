alter table daily_submissions add column if not exists admissions integer not null default 0;
alter table daily_submissions add column if not exists discharges integer not null default 0;
alter table daily_submissions add column if not exists surgeries integer not null default 0;
alter table daily_submissions add column if not exists deliveries integer not null default 0;
alter table daily_submissions add column if not exists critical_results_count integer not null default 0;
alter table daily_submissions add column if not exists staffing_shortfall_flag boolean not null default false;
alter table daily_submissions add column if not exists crowding_flag boolean not null default false;
alter table daily_submissions add column if not exists system_downtime_flag boolean not null default false;

create table if not exists event_cases (
  case_id text primary key,
  source_mode text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  facility_id text not null references facilities(facility_id) on delete cascade,
  department_id text references departments(department_id) on delete set null,
  report_id text references event_reports(report_id) on delete set null,
  event_timestamp timestamptz not null,
  encounter_setting text not null,
  shift text not null default 'unknown',
  patient_age_band text not null,
  patient_sex text not null,
  special_population_flags jsonb not null default '[]'::jsonb,
  encounter_id_local text,
  high_risk_flag boolean not null default false,
  domain text not null,
  deviation_class text not null,
  process_stage text not null,
  event_type text not null,
  actual_harm text not null,
  potential_harm text not null,
  severity_level text not null,
  preventability_rating text not null,
  detectability_rating text not null,
  recurrence_flag boolean not null default false,
  event_summary text not null,
  what_was_expected text not null,
  what_happened text not null,
  immediate_action_taken text not null,
  evidence_source text not null,
  linked_system_trace_id text,
  linked_policy_version text,
  contributing_factors jsonb not null default '[]'::jsonb,
  triage_status text not null default 'new',
  investigation_method text not null default 'desk review',
  root_cause_category text,
  corrective_action text,
  preventive_action text,
  owner_assigned text,
  due_date date,
  closure_status text not null default 'open',
  closure_date date,
  closure_quality_rating text,
  ai_summary text,
  ai_confidence double precision,
  ai_provider text,
  ai_model text,
  ai_human_override text
);

create table if not exists ai_provider_configs (
  config_id text primary key,
  owner_user_id text not null references surveillance_users(user_id) on delete cascade,
  provider text not null,
  label text not null,
  model text not null,
  base_url text not null,
  api_key_ciphertext text not null,
  api_key_masked text not null,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_event_cases_facility_timestamp on event_cases (facility_id, event_timestamp desc);
create index if not exists idx_event_cases_status on event_cases (triage_status, closure_status);
create index if not exists idx_event_cases_domain on event_cases (domain, deviation_class);
create index if not exists idx_ai_provider_configs_owner_active on ai_provider_configs (owner_user_id, is_active);
