create extension if not exists pgcrypto;

create table if not exists events (
  id uuid primary key default gen_random_uuid(),
  event_id text unique not null,
  encounter_id text not null,
  patient_id text not null,
  event_type text not null,
  event_time timestamptz not null,
  source_system text not null default 'synthetic',
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists alerts (
  id uuid primary key default gen_random_uuid(),
  alert_id text unique not null,
  encounter_id text not null,
  patient_id text not null,
  domain text not null,
  alert_type text not null,
  severity text not null,
  confidence_score double precision not null,
  evidence jsonb not null default '{}'::jsonb,
  recommended_action jsonb not null default '{}'::jsonb,
  status text not null default 'open',
  routed_to jsonb not null default '[]'::jsonb,
  generated_at timestamptz not null,
  created_at timestamptz not null default now()
);

create table if not exists agent_tasks (
  id uuid primary key default gen_random_uuid(),
  task_id text unique not null,
  owner_agent text not null,
  task_name text not null,
  status text not null,
  details jsonb not null default '{}'::jsonb,
  created_at timestamptz not null,
  completed_at timestamptz
);

create table if not exists review_actions (
  id uuid primary key default gen_random_uuid(),
  action_id text unique not null,
  alert_id text not null,
  acted_by text not null,
  acted_at timestamptz not null,
  action_type text not null,
  override_reason text,
  comment text
);

