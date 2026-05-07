# ============================================================
# Push woocommerce-erp-integration post to WordPress as draft
# Run this from PowerShell:
#   cd C:\content-intel
#   .\clients\virtina\output\research\push_erp_post_final.ps1
# ============================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# --- Load credentials from .env ---
$envPath = "C:\content-intel\.env"
$creds = @{}
Get-Content $envPath | ForEach-Object {
    $line = $_.Trim()
    if ($line -and $line -notmatch '^#' -and $line -match '^(.+?)=(.*)$') {
        $creds[$Matches[1].Trim()] = $Matches[2].Trim()
    }
}
$WP_USERNAME   = $creds['WP_USERNAME']
$WP_APP_PASS   = $creds['WP_APP_PASSWORD']

# Build Basic Auth header
$credStr   = "${WP_USERNAME}:${WP_APP_PASS}"
$b64       = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($credStr))
$authValue = "Basic $b64"

Write-Host "Credentials loaded. Username: $WP_USERNAME"

# --- Read post content (strip YAML frontmatter) ---
$publishedFile = "C:\content-intel\clients\virtina\output\published\woocommerce-erp-integration-2026-05-07.md"
$raw = Get-Content -Path $publishedFile -Raw -Encoding UTF8

# Frontmatter is between first and second '---'
# Split into max 3 parts on '---'
$splitContent = $raw -split '(?m)^---\s*$', 3
# $splitContent[0] = empty or whitespace
# $splitContent[1] = frontmatter
# $splitContent[2] = post body
if ($splitContent.Count -lt 3) {
    Write-Error "Could not parse frontmatter from published file."
    exit 1
}
$postContent = $splitContent[2].Trim()
Write-Host "Post content length: $($postContent.Length) chars"

# --- Validate key fields ---
$seoTitle   = "WooCommerce ERP integration for B2B manufacturers | Virtina"
$metaDesc   = "Learn how to connect WooCommerce to your ERP. A guide for B2B manufacturers and distributors covering data mapping, sync strategy, and connector selection."
$focusKw    = "WooCommerce ERP integration"

Write-Host "SEO title ($($seoTitle.Length) chars): $seoTitle"
Write-Host "Meta desc ($($metaDesc.Length) chars): $metaDesc"

if ($seoTitle.Length -gt 60) { Write-Warning "SEO title exceeds 60 chars!" }
if ($metaDesc.Length -lt 150 -or $metaDesc.Length -gt 160) { Write-Warning "Meta desc is $($metaDesc.Length) chars (target 150-160)!" }

# --- Build JSON payload ---
$payload = [ordered]@{
    title          = "How to connect WooCommerce to your ERP: a practical guide for B2B manufacturers and distributors"
    slug           = "woocommerce-erp-integration"
    status         = "draft"
    content        = $postContent
    featured_media = 0
    categories     = @(79, 84)
    author         = 9
    meta           = [ordered]@{
        "_yoast_wpseo_title"    = $seoTitle
        "_yoast_wpseo_metadesc" = $metaDesc
        "_yoast_wpseo_focuskw"  = $focusKw
    }
}

$payloadJson  = $payload | ConvertTo-Json -Depth 10 -Compress
$payloadBytes = [System.Text.Encoding]::UTF8.GetBytes($payloadJson)
Write-Host "Payload size: $($payloadBytes.Length) bytes"

# --- POST to WordPress ---
$endpoint = "https://virtina.com/wp-json/wp/v2/posts"
Write-Host "`nPosting to $endpoint ..."

try {
    $response = Invoke-RestMethod `
        -Uri        $endpoint `
        -Method     POST `
        -Headers    @{ Authorization = $authValue } `
        -ContentType "application/json; charset=utf-8" `
        -Body       $payloadBytes `
        -TimeoutSec 120

    $postId   = $response.id
    $postLink = $response.link
    $editUrl  = "https://virtina.com/wp-admin/post.php?post=$postId&action=edit"

    Write-Host "`n=== SUCCESS ===" -ForegroundColor Green
    Write-Host "Post ID  : $postId"
    Write-Host "Post URL : $postLink"
    Write-Host "Edit URL : $editUrl"

    # Save full response
    $respPath = "C:\content-intel\clients\virtina\output\research\push_erp_response.json"
    $response | ConvertTo-Json -Depth 20 | Out-File -FilePath $respPath -Encoding UTF8
    Write-Host "Response : $respPath"

    # Save post ID for next step
    "$postId" | Out-File -FilePath "C:\content-intel\clients\virtina\output\research\erp_post_id.txt" -Encoding UTF8

    # Patch the published file frontmatter with the new post ID
    $pubContent = Get-Content -Path $publishedFile -Raw -Encoding UTF8
    $pubContent = $pubContent -replace 'wp_post_id: PENDING_PUSH', "wp_post_id: $postId"
    $pubContent = $pubContent -replace 'canonical_url:', "canonical_url: $postLink"
    [System.IO.File]::WriteAllText($publishedFile, $pubContent, [System.Text.Encoding]::UTF8)
    Write-Host "Published file updated with post ID and canonical URL."

} catch [System.Net.WebException] {
    $ex = $_.Exception
    Write-Host "`n=== FAILED ===" -ForegroundColor Red
    Write-Host "HTTP Error: $($ex.Message)"
    if ($ex.Response) {
        $stream = $ex.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $errBody = $reader.ReadToEnd()
        Write-Host "Response body (first 3000 chars):"
        Write-Host $errBody.Substring(0, [Math]::Min(3000, $errBody.Length))
        $errPath = "C:\content-intel\clients\virtina\output\research\push_erp_error.txt"
        $errBody | Out-File -FilePath $errPath -Encoding UTF8
        Write-Host "Full error saved to $errPath"
    }
} catch {
    Write-Host "`n=== FAILED ===" -ForegroundColor Red
    Write-Host "Exception: $($_.Exception.GetType().Name): $($_.Exception.Message)"
}
