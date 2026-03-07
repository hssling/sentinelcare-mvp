param(
  [Parameter(Mandatory = $true)][string]$Repo,
  [Parameter(Mandatory = $true)][string]$NetlifyAuthToken,
  [Parameter(Mandatory = $true)][string]$NetlifySiteId,
  [Parameter(Mandatory = $true)][string]$SupabaseProjectRef,
  [Parameter(Mandatory = $true)][string]$SupabaseAccessToken,
  [Parameter(Mandatory = $true)][string]$SupabaseDbPassword,
  [Parameter(Mandatory = $true)][string]$ViteSupabaseUrl,
  [Parameter(Mandatory = $true)][string]$ViteSupabaseAnonKey
)

gh secret set NETLIFY_AUTH_TOKEN --repo $Repo --body $NetlifyAuthToken
gh secret set NETLIFY_SITE_ID --repo $Repo --body $NetlifySiteId
gh secret set SUPABASE_PROJECT_REF --repo $Repo --body $SupabaseProjectRef
gh secret set SUPABASE_ACCESS_TOKEN --repo $Repo --body $SupabaseAccessToken
gh secret set SUPABASE_DB_PASSWORD --repo $Repo --body $SupabaseDbPassword
gh secret set VITE_SUPABASE_URL --repo $Repo --body $ViteSupabaseUrl
gh secret set VITE_SUPABASE_ANON_KEY --repo $Repo --body $ViteSupabaseAnonKey

Write-Host "GitHub Actions secrets configured for $Repo"

