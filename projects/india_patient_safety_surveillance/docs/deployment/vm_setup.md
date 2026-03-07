# VM Setup

1. Install Python 3.11, git, and nginx.
2. Clone repository and run `pip install .` in a virtual environment.
3. Start API with:
   - `uvicorn indiasurveillance.api:app --host 127.0.0.1 --port 8010`
4. Reverse proxy through nginx on ports 80 and 443.
5. Point frontend build variable `VITE_INDIA_SURVEILLANCE_API_BASE` to the public API URL.
