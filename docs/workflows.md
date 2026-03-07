# Workflows

## Core patient safety workflow

1. Ingest event.
2. Normalize and classify event.
3. Execute multi-domain detection.
4. Route alert by severity and domain.
5. Capture human review action.
6. Persist evidence and audit logs.

## Multi-agent workflow

1. Agent A: scope/boundary check.
2. Agent B: rule-context preparation.
3. Agent C: interoperability normalization.
4. Agent D: detection execution.
5. Agent E: safety sanity challenge.
6. Agent F: alert routing and notification ownership.
7. Agent G: DevSecOps/MLOps audit registration.
8. Agent H: validation/documentation registration.

## Release workflow

1. Developer pushes from IDE to GitHub branch.
2. CI runs backend tests and frontend build.
3. Merge to `main`.
4. Netlify production deploy runs automatically.
5. Supabase migration workflow applies schema changes.
6. API image workflow publishes latest backend image.

