# Push woocommerce-erp-integration post to WordPress as draft
# Run from: C:\content-intel

$envFile = "C:\content-intel\.env"
$envVars = @{}
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^([^#][^=]*)=(.*)$') {
        $envVars[$matches[1].Trim()] = $matches[2].Trim()
    }
}

$WP_USERNAME = $envVars['WP_USERNAME']
$WP_APP_PASSWORD = $envVars['WP_APP_PASSWORD']

$bytes = [System.Text.Encoding]::UTF8.GetBytes("${WP_USERNAME}:${WP_APP_PASSWORD}")
$base64 = [Convert]::ToBase64String($bytes)
$authHeader = "Basic $base64"

Write-Host "Username: $WP_USERNAME"
Write-Host "Auth token built (length: $($base64.Length) chars)"

# Read published file and strip frontmatter
$publishedPath = "C:\content-intel\clients\virtina\output\published\woocommerce-erp-integration-2026-05-07.md"
$rawContent = Get-Content -Path $publishedPath -Raw -Encoding UTF8

# Split on --- to remove frontmatter
$parts = $rawContent -split '---', 3
$postContent = $parts[2].Trim()

Write-Host "Content length: $($postContent.Length) chars"

# Build payload
$payload = @{
    title = "How to connect WooCommerce to your ERP: a practical guide for B2B manufacturers and distributors"
    slug = "woocommerce-erp-integration"
    status = "draft"
    content = $postContent
    featured_media = 0
    categories = @(79, 84)
    author = 9
    meta = @{
        "_yoast_wpseo_title" = "WooCommerce ERP integration for B2B manufacturers | Virtina"
        "_yoast_wpseo_metadesc" = "Learn how to connect WooCommerce to your ERP. A guide for B2B manufacturers and distributors covering data mapping, sync strategy, and connector selection."
        "_yoast_wpseo_focuskw" = "WooCommerce ERP integration"
    }
}

$payloadJson = $payload | ConvertTo-Json -Depth 10 -Compress

Write-Host "Payload JSON size: $($payloadJson.Length) bytes"
Write-Host "SEO title length: $($payload.meta.'_yoast_wpseo_title'.Length) chars"
Write-Host "Meta desc length: $($payload.meta.'_yoast_wpseo_metadesc'.Length) chars"
Write-Host ""
Write-Host "Posting to: https://virtina.com/wp-json/wp/v2/posts"

try {
    $response = Invoke-RestMethod `
        -Uri "https://virtina.com/wp-json/wp/v2/posts" `
        -Method POST `
        -Headers @{ Authorization = $authHeader; "Content-Type" = "application/json; charset=utf-8" } `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($payloadJson)) `
        -TimeoutSec 120

    $postId = $response.id
    $postLink = $response.link
    Write-Host ""
    Write-Host "SUCCESS"
    Write-Host "Post ID: $postId"
    Write-Host "Post link: $postLink"
    Write-Host "Edit URL: https://virtina.com/wp-admin/post.php?post=$postId&action=edit"

    # Save response
    $response | ConvertTo-Json -Depth 10 | Out-File -FilePath "C:\content-intel\clients\virtina\output\research\push_erp_response.json" -Encoding UTF8
    Write-Host "Response saved to push_erp_response.json"

    # Write post ID for reference
    "$postId" | Out-File -FilePath "C:\content-intel\clients\virtina\output\research\erp_post_id.txt" -Encoding UTF8

} catch {
    Write-Host ""
    Write-Host "FAILED: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $errorBody = $reader.ReadToEnd()
        Write-Host "Error body: $($errorBody.Substring(0, [Math]::Min(2000, $errorBody.Length)))"
        $errorBody | Out-File -FilePath "C:\content-intel\clients\virtina\output\research\push_erp_error.txt" -Encoding UTF8
        Write-Host "Error saved to push_erp_error.txt"
    }
}
