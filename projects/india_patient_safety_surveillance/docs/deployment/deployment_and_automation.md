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

## GitHub secrets for automation

1. `VITE_INDIA_SURVEILLANCE_API_BASE`
2. `NETLIFY_INDIA_SURVEILLANCE_AUTH_TOKEN`
3. `NETLIFY_INDIA_SURVEILLANCE_SITE_ID`

## Deployment verification

1. API health: `/health`
2. Frontend build success
3. Trace endpoint returns report path
4. UI shows `Live API demo`
