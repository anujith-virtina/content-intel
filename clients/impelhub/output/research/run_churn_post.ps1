Set-Location "C:\content-intel"

# Load .env
Get-Content "C:\content-intel\.env" | ForEach-Object {
    if ($_ -match '^\s*([^#=][^=]*)=(.*)$') {
        $key = $matches[1].Trim()
        $val = $matches[2].Trim()
        [System.Environment]::SetEnvironmentVariable($key, $val, 'Process')
    }
}

Write-Host "IMPELHUB_WP_USERNAME=$env:IMPELHUB_WP_USERNAME"
$pexelsKey = $env:PEXELS_API_KEY
if ($pexelsKey) {
    Write-Host "PEXELS_API_KEY=$($pexelsKey.Substring(0, [Math]::Min(8, $pexelsKey.Length)))... (present)"
} else {
    Write-Host "PEXELS_API_KEY=not set (will use Openverse fallback)"
}

python "C:\content-intel\clients\impelhub\output\research\publish_churn_post.py" 2>&1 | Tee-Object -FilePath "C:\content-intel\clients\impelhub\output\research\churn_post_build_log.txt"
