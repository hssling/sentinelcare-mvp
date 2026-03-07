create table if not exists facilities (
  facility_id text primary key,
  name text not null,
  state text not null,
  district text not null,
  ownership text not null,
  level text not null,
  abdm_registry_ready boolean not null default false,
  registry_source text not null default 'manual'
);

create table if not exists departments (
  department_id text primary key,
  facility_id text not null references facilities(facility_id) on delete cascade,
  name text not null,
  category text not null,
  reporting_enabled boolean not null default true
);

create table if not exists surveillance_users (
  user_id text primary key,
  name text not null,
  username text not null unique,
  role text not null,
  state text,
  district text,
  facility_id text references facilities(facility_id) on delete set null,
  department_id text references departments(department_id) on delete set null,
  is_active boolean not null default true,
  password_hash text not null,
  password_salt text not null,
  created_at timestamptz not null default now(),
  created_by text
);

create table if not exists state_cells (
  state_cell_id text primary key,
  state text not null,
  nodal_unit text not null,
  lead_name text not null,
  status text not null,
  facilities_mapped integer not null default 0
);

create table if not exists policies (
  policy_id text primary key,
  title text not null,
  state text not null,
  validation_phase text not null,
  approver text not null,
  activation_scope text not null,
  last_updated date not null
);

create table if not exists event_reports (
  report_id text primary key,
  event_date date not null,
  reported_at timestamptz not null,
  facility_id text not null references facilities(facility_id) on delete cascade,
  patient_context text not null,
  domain text not null,
  deviation_class text not null,
  severity text not null,
  process_stage text not null,
  summary text not null,
  immediate_action text not null,
  status text not null,
  assigned_to text,
  state_cell text,
  closure_note text
);

create table if not exists safety_signals (
  signal_id text primary key,
  title text not null,
  scope text not null,
  state text,
  district text,
  domain text not null,
  deviation_class text not null,
  severity text not null,
  reports_linked integer not null default 0,
  owner_role text not null,
  next_action text not null,
  status text not null
);

create table if not exists daily_submissions (
  submission_id text primary key,
  submission_date date not null,
  facility_id text not null references facilities(facility_id) on delete cascade,
  department_id text not null references departments(department_id) on delete cascade,
  submitted_by text not null,
  patient_days integer not null default 0,
  near_misses integer not null default 0,
  no_harm_events integer not null default 0,
  harm_events integer not null default 0,
  severe_events integer not null default 0,
  medication_events integer not null default 0,
  procedure_events integer not null default 0,
  infection_events integer not null default 0,
  diagnostic_events integer not null default 0,
  escalation_required boolean not null default false,
  notes text not null default '',
  reviewed_by text,
  review_status text not null default 'submitted',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists notifications (
  notification_id text primary key,
  created_at timestamptz not null default now(),
  user_id text,
  scope text not null,
  title text not null,
  message text not null,
  severity text not null,
  status text not null default 'open',
  facility_id text references facilities(facility_id) on delete set null,
  state text,
  entity_type text,
  entity_id text
);

create table if not exists audit_logs (
  audit_id text primary key,
  created_at timestamptz not null default now(),
  actor_user_id text,
  action text not null,
  entity_type text not null,
  entity_id text not null,
  detail text not null
);

create index if not exists idx_daily_submissions_facility_date on daily_submissions (facility_id, submission_date);
create index if not exists idx_daily_submissions_department_date on daily_submissions (department_id, submission_date);
create index if not exists idx_event_reports_facility_date on event_reports (facility_id, event_date);
create index if not exists idx_notifications_user_status on notifications (user_id, status);
create index if not exists idx_audit_logs_created_at on audit_logs (created_at desc);
