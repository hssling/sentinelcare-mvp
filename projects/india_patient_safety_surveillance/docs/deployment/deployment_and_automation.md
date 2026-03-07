# Deployment and Automation

## Frontend deployment

Target: Netlify

### Build settings

- Base directory: `frontend/india-surveillance`
- Build command: `npm run build`
- Publish directory: `dist`
- Environment variable:
  - `VITE_INDIA_SURVEILLANCE_API_BASE`

## Backend deployment

Recommended targets:

1. Render web service using `projects/india_patient_safety_surveillance/render.yaml`
2. VM deployment using `uvicorn indiasurveillance.api:app --host 0.0.0.0 --port 8010`
3. Supabase as the persistent operational database

### Required backend environment

- `SUPABASE_INDIA_URL`
- `SUPABASE_INDIA_SERVICE_ROLE_KEY`
- `INDIA_SURVEILLANCE_JWT_SECRET`

### Database migration

- Migration path: `projects/india_patient_safety_surveillance/supabase/migrations/001_init.sql`
- Automation workflow: `.github/workflows/india-surveillance-supabase-db.yml`
- Execution helper: `scripts/execute_supabase_sql.py`

## GitHub secrets for automation

1. `VITE_INDIA_SURVEILLANCE_API_BASE`
2. `NETLIFY_INDIA_SURVEILLANCE_AUTH_TOKEN`
3. `NETLIFY_INDIA_SURVEILLANCE_SITE_ID`
4. `SUPABASE_INDIA_ACCESS_TOKEN`
5. `SUPABASE_INDIA_PROJECT_REF`
6. `SUPABASE_INDIA_URL`
7. `SUPABASE_INDIA_SERVICE_ROLE_KEY`
8. `SUPABASE_INDIA_ANON_KEY`
9. `INDIA_SURVEILLANCE_JWT_SECRET`
10. `INDIA_VM_HOST`
11. `INDIA_VM_USER`
12. `INDIA_VM_SSH_KEY`
13. `INDIA_VM_SSH_PASSPHRASE` if the private key is encrypted

### API VM deployment workflow

- Workflow: `.github/workflows/deploy-india-surveillance-api-vm.yml`
- The VM deploy workflow expects SSH key-based access and writes `.env.india` on the host before restarting the API.

## Deployment verification

1. API health: `/health`
2. Frontend build success
3. `/auth/login` returns JWT bearer token
4. `/dashboard`, `/notifications`, `/audit-logs`, and `/trends` return authenticated data
5. Trace endpoint returns report path
6. UI shows live role dashboards rather than demo-only placeholders
