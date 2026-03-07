# Netlify + Supabase Deployment

## Architecture

- Netlify hosts the React command console (`frontend/web`).
- Supabase stores events, alerts, tasks, and review actions.
- FastAPI runs as API service (local, container host, or managed runtime) and writes to Supabase with service role key.

## Supabase setup

1. Create Supabase project.
2. Apply migration:
   - `supabase/migrations/001_init.sql`
3. Enable Row Level Security and policies as required for production.

## Netlify setup

1. Connect GitHub repo to Netlify site.
2. Build settings:
   - Base directory: `frontend/web`
   - Build command: `npm ci && npm run build`
   - Publish directory: `dist`
3. Set env vars:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
   - `VITE_API_BASE_URL` (FastAPI base URL, e.g. `https://<api-host>`)

## Backend setup

1. Set API env vars:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
2. Run API:
   - `uvicorn sentinelcare.api:app --host 0.0.0.0 --port 8000`
3. Optionally deploy container from GHCR image published by workflow.

## GitHub secrets checklist

- `NETLIFY_AUTH_TOKEN`
- `NETLIFY_SITE_ID`
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`
- `VITE_API_BASE_URL`
- `SUPABASE_ACCESS_TOKEN`
- `SUPABASE_PROJECT_REF`
- `SUPABASE_DB_PASSWORD`
