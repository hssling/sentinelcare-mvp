# CI/CD and Automation

## Objective

Single push from IDE triggers validation and deployment workflows across frontend, data layer, and backend artifact pipelines.

## GitHub workflows

### `ci.yml`

- Triggers: push (`main`, `develop`) and pull request.
- Backend job:
  - install with `pip install -e .[dev]`
  - run `pytest`
- Frontend job:
  - install with `npm ci`
  - run `npm run build`

### `deploy-netlify.yml`

- Triggers: push to `main`, manual dispatch.
- Builds React frontend and deploys to Netlify production.
- Required secrets:
  - `NETLIFY_AUTH_TOKEN`
  - `NETLIFY_SITE_ID`
  - `VITE_SUPABASE_URL`
  - `VITE_SUPABASE_ANON_KEY`

### `supabase-db.yml`

- Triggers: push to `main` for `supabase/**`, manual dispatch.
- Links Supabase project and runs migration push.
- Required secrets:
  - `SUPABASE_ACCESS_TOKEN`
  - `SUPABASE_PROJECT_REF`
  - `SUPABASE_DB_PASSWORD`

### `deploy-api-image.yml`

- Triggers: backend-related changes on `main`, manual dispatch.
- Builds and pushes `ghcr.io/<owner>/sentinelcare-api:latest`.

## Branch strategy

1. `develop` for integration testing.
2. `main` for production deploy triggers.
3. Feature branches for isolated changes with PR checks.

