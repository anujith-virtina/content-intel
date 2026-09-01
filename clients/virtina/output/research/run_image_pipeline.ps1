# Run Virtina image fetch + upload pipeline
# Loads credentials from .env and runs the Python script

$envFile = "C:\content-intel\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | Where-Object { $_ -match "^\s*[A-Z_]+=.+" } | ForEach-Object {
        $parts = $_ -split "=", 2
        $name = $parts[0].Trim()
        $value = $parts[1].Trim()
        [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
        Write-Host "Loaded: $name"
    }
} else {
    Write-Error ".env file not found at $envFile"
    exit 1
}

Write-Host "WP_USERNAME: $env:WP_USERNAME"
Write-Host "Running image pipeline..."

python "C:\content-intel\clients\virtina\output\research\image_fetch_upload.py"
