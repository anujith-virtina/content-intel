# Load .env and run the full publish pipeline
$envFile = "C:\content-intel\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | Where-Object { $_ -notmatch "^\s*#" -and $_ -match "=" } | ForEach-Object {
        $parts = $_ -split "=", 2
        if ($parts.Count -eq 2) {
            $name = $parts[0].Trim()
            $value = $parts[1].Trim()
            [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    Write-Host "Credentials loaded from .env"
} else {
    Write-Error ".env not found"
    exit 1
}

Write-Host "WP_USERNAME=$env:WP_USERNAME"
Write-Host "Pexels key set: $(if ($env:PEXELS_API_KEY) { 'YES' } else { 'NO (will use Openverse)' })"

python "C:\content-intel\clients\virtina\output\research\publish_b2b_portal.py"
