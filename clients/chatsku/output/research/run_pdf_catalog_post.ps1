Set-Location "C:\content-intel"

# Load .env
Get-Content "C:\content-intel\.env" | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
    }
}

Write-Host "CHATSKU_WP_USERNAME=$env:CHATSKU_WP_USERNAME"
$pexelsKey = $env:PEXELS_API_KEY
if ($pexelsKey) {
    Write-Host "PEXELS_API_KEY=$($pexelsKey.Substring(0, [Math]::Min(8, $pexelsKey.Length)))... (present)"
} else {
    Write-Host "PEXELS_API_KEY=not set (will use Openverse fallback)"
}

python "C:\content-intel\clients\chatsku\output\research\build_pdf_catalog_post.py" 2>&1 | Tee-Object -FilePath "C:\content-intel\clients\chatsku\output\research\pdf_catalog_build_log.txt"
