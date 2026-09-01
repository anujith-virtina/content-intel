# Run the B2B catalog conversion rate post build script
# PowerShell

Set-Location C:\content-intel

# Load .env
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.+)$') {
        $key = $matches[1].Trim()
        $val = $matches[2].Trim()
        [System.Environment]::SetEnvironmentVariable($key, $val, 'Process')
    }
}

Write-Host "Credentials loaded:"
Write-Host "  CHATSKU_WP_USERNAME = $env:CHATSKU_WP_USERNAME"
Write-Host "  PEXELS_API_KEY = $(if ($env:PEXELS_API_KEY) { 'set' } else { 'not set (Openverse fallback)' })"

python clients\chatsku\output\research\build_b2b_catalog_conversion_post.py
