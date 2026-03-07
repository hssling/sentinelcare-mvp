# Render Setup

1. Create a new Render Web Service.
2. Connect this repository.
3. Use `projects/india_patient_safety_surveillance/render.yaml` or set manually:
   - Build command: `pip install --upgrade pip && pip install .`
   - Start command: `uvicorn indiasurveillance.api:app --host 0.0.0.0 --port $PORT`
4. Health check: `/health`
5. After deploy, set the Netlify build variable:
   - `VITE_INDIA_SURVEILLANCE_API_BASE=https://<render-service>.onrender.com`
