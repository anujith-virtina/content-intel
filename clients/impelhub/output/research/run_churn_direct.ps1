Set-Location "C:\content-intel"

# Load .env
Get-Content "C:\content-intel\.env" | ForEach-Object {
    if ($_ -match '^\s*([^#=][^=]*)=(.*)$') {
        $key = $matches[1].Trim()
        $val = $matches[2].Trim()
        [System.Environment]::SetEnvironmentVariable($key, $val, 'Process')
    }
}

Write-Host "Credentials loaded:"
Write-Host "  IMPELHUB_WP_USERNAME=$env:IMPELHUB_WP_USERNAME"
Write-Host "  IMPELHUB_WP_APP_PASSWORD=$(if ($env:IMPELHUB_WP_APP_PASSWORD) { 'SET' } else { 'NOT SET' })"

python "C:\content-intel\clients\impelhub\output\research\publish_churn_direct.py" 2>&1 | Tee-Object -FilePath "C:\content-intel\clients\impelhub\output\research\churn_direct_log.txt"
