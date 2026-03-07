# IDE to Production Automation

## One-time setup

1. Create GitHub repository and push this codebase.
2. Create Netlify site and Supabase project.
3. Install CLI tools locally:
   - `gh`
   - `supabase`
4. Set GitHub Actions secrets:
   - run [bootstrap_github_automation.ps1](/d:/Medical%20Error%20U-HEDPPLS/scripts/bootstrap_github_automation.ps1) or configure in UI.

## Daily developer flow

1. Develop in IDE.
2. Commit and push feature branch.
3. Open PR -> CI validates backend and frontend.
4. Merge to `main`.
5. Automated outcomes:
   - Netlify deploy updates production web app.
   - Supabase migration workflow applies DB changes.
   - API image is published to GHCR.

## Local pre-push checks

1. `python -m pytest -q`
2. `cd frontend/web && npm run build`

