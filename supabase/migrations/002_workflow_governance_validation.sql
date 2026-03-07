create table if not exists workflow_queue (
  id uuid primary key default gen_random_uuid(),
  queue_id text unique not null,
  alert_id text not null,
  encounter_id text not null,
  patient_id text not null,
  priority text not null,
  assigned_role text not null,
  due_at timestamptz not null,
  status text not null default 'open',
  escalation_level integer not null default 0,
  created_at timestamptz not null,
  updated_at timestamptz not null
);

create table if not exists policy_versions (
  id uuid primary key default gen_random_uuid(),
  policy_id text unique not null,
  policy_name text not null,
  version text not null,
  status text not null,
  definition jsonb not null default '{}'::jsonb,
  submitted_by text not null,
  approved_by text,
  approved_at timestamptz,
  created_at timestamptz not null
);

create table if not exists validation_reports (
  id uuid primary key default gen_random_uuid(),
  report_id text unique not null,
  report_type text not null,
  generated_at timestamptz not null,
  payload jsonb not null default '{}'::jsonb
);

