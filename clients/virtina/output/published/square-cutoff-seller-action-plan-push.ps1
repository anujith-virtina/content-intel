# Push: "Square is closing hemp and CBD accounts" -> virtina.com as DRAFT
# Run from project root:  powershell -ExecutionPolicy Bypass -File .\clients\virtina\output\published\square-cutoff-seller-action-plan-push.ps1
# Creates the post, then re-fetches with context=edit and verifies the saved content.

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$root        = 'C:\content-intel'
$contentPath = Join-Path $root 'clients\virtina\output\published\square-cutoff-seller-action-plan-content.html'
$envPath     = Join-Path $root '.env'

# ---------- credentials ----------
if (-not (Test-Path $envPath)) { throw ".env not found at $envPath" }
Get-Content $envPath | ForEach-Object {
  if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
    $k = $Matches[1]; $v = $Matches[2].Trim().Trim('"').Trim("'")
    Set-Item -Path ("Env:" + $k) -Value $v
  }
}
$user = $env:WP_USERNAME
$pass = $env:WP_APP_PASSWORD
if ([string]::IsNullOrWhiteSpace($user) -or [string]::IsNullOrWhiteSpace($pass)) {
  throw "WP_USERNAME / WP_APP_PASSWORD missing from .env"
}
$basic = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$user`:$pass"))

# Full browser UA - a short UA gets a Wordfence 403 on this host.
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
$headers = @{
  Authorization = "Basic $basic"
  'User-Agent'  = $ua
  Accept        = 'application/json'
}

# ---------- content ----------
$content = [IO.File]::ReadAllText($contentPath, [Text.Encoding]::UTF8)

# ---------- pre-flight gates (Wordfence + house rules) ----------
if ($content -match '<!--')                                  { throw 'GATE FAIL: HTML comment present (Wordfence 403 risk).' }
if ($content -match "$([char]0x2014)|&mdash;|&#8212;|&#x2014;") { throw 'GATE FAIL: em dash present.' }
if ($content -match '<<|>>')                                 { throw 'GATE FAIL: orphan angle-bracket fragment.' }
if ($content -match 'placehold\.co|source\.unsplash\.com')   { throw 'GATE FAIL: placeholder image URL.' }
if ($content -match 'none !important')                       { throw 'GATE FAIL: space before !important.' }
$extCount = ([regex]::Matches($content,'href="https?://(?!virtina\.com)')).Count
if ($extCount -gt 2) { throw "GATE FAIL: $extCount external links (cap is 2)." }
$badInternal = [regex]::Matches($content,'href="https://virtina\.com/[^"]*"\s+target=').Count
if ($badInternal -gt 0) { throw "GATE FAIL: $badInternal internal link(s) carry target." }
Write-Host "Pre-flight gates: PASS (external links = $extCount, content chars = $($content.Length))"

# ---------- payload ----------
$payload = [ordered]@{
  title          = 'Square is closing hemp and CBD accounts: what happens to your money, your data, and your catalog'
  slug           = 'square-cutoff-seller-action-plan'
  status         = 'draft'
  content        = $content
  excerpt        = 'Square is closing hemp and CBD accounts on two dates, and the federal hemp law now lands on two more. Which dates are yours, and what to do first.'
  author         = 9
  categories     = @(405, 79)
  tags           = @(19, 37, 321, 385)
  comment_status = 'closed'
  meta           = [ordered]@{
    '_yoast_wpseo_title'    = 'Square Hemp and CBD Account Closure: Seller Plan | Virtina'
    '_yoast_wpseo_metadesc' = 'Square is closing hemp and CBD accounts on two dates, and the federal hemp law now lands on two more. Find out which dates are yours and what to do first.'
    '_yoast_wpseo_focuskw'  = 'Square hemp and CBD account closure'
  }
}
# featured_media deliberately NOT sent: no image sourced, no Pexels key. Set it manually.

$json  = $payload | ConvertTo-Json -Depth 6 -Compress
$bytes = [Text.Encoding]::UTF8.GetBytes($json)

# ---------- POST ----------
$create = 'https://virtina.com/wp-json/wp/v2/posts'
try {
  $resp = Invoke-RestMethod -Uri $create -Method Post -Headers $headers -ContentType 'application/json; charset=utf-8' -Body $bytes
} catch {
  $code = $null
  if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode }
  Write-Host "POST FAILED. HTTP $code"
  Write-Host $_.Exception.Message
  Write-Host "If 403: Wordfence. Bisect the body, do NOT retry blindly."
  throw
}
$postId = $resp.id
Write-Host "CREATED post id=$postId status=$($resp.status) slug=$($resp.slug)"
Write-Host "Edit URL: https://virtina.com/wp-admin/post.php?post=$postId&action=edit"

# ---------- verify with context=edit ----------
Start-Sleep -Seconds 3
$verifyUrl = "https://virtina.com/wp-json/wp/v2/posts/$postId" + '?context=edit&_fields=id,slug,status,title,featured_media,categories,tags,author,content,meta,link'
$v = Invoke-RestMethod -Uri $verifyUrl -Method Get -Headers $headers
$saved = $v.content.raw

Write-Host ''
Write-Host '--- SAVED-CONTENT VERIFICATION ---'
Write-Host ("sent chars        : {0}" -f $content.Length)
Write-Host ("saved chars       : {0}" -f $saved.Length)
Write-Host ("exact match       : {0}" -f ($saved -eq $content))
Write-Host ("status            : {0}" -f $v.status)
Write-Host ("slug              : {0}" -f $v.slug)
Write-Host ("author            : {0}" -f $v.author)
Write-Host ("categories        : {0}" -f ($v.categories -join ','))
Write-Host ("tags              : {0}" -f ($v.tags -join ','))
Write-Host ("featured_media    : {0}" -f $v.featured_media)
Write-Host ''
Write-Host '--- STRUCTURE SPOT CHECKS ON SAVED CONTENT ---'
$checks = [ordered]@{
  'TOC ul has list-style:none!important' = ($saved -match 'list-style:none!important')
  'TOC SVG arrows fill #43627f (10)'     = ([regex]::Matches($saved,'fill:#43627f;').Count -ge 10)
  'no Unicode arrow in TOC'              = (-not ($saved -match [char]0x2192))
  'H2 anchor ids (10)'                   = ([regex]::Matches($saved,'<h2 id="').Count -eq 10)
  'H3 22px slate (23 = 1 TOC + 22 body)' = ([regex]::Matches($saved,'<h3 style="color:#43627f;font-size:22px;">').Count -eq 23)
  'bullet circles #43627f (25)'          = ([regex]::Matches($saved,'background-color:#43627f;border-radius:50%').Count -eq 25)
  'bullet text spans 16px (25)'          = ([regex]::Matches($saved,'font-size:16px;line-height:1.75;color:#2d3e50').Count -eq 25)
  'body ul Template F (6)'               = ([regex]::Matches($saved,'<ul style="list-style:none;padding-left:4px').Count -eq 6)
  'internal links (9)'                   = ([regex]::Matches($saved,'href="https://virtina\.com/').Count -eq 9)
  'external links (2)'                   = ([regex]::Matches($saved,'target="_blank" rel="noopener noreferrer"').Count -eq 2)
  'FAQ details items (6)'                = ([regex]::Matches($saved,'<details class="vfaq"').Count -eq 6)
  'conclusion teal box'                  = ($saved -match 'background:#00d5c0;border-radius:20px')
  'no em dash'                           = (-not ($saved -match [char]0x2014))
  'no << or >>'                          = (-not ($saved -match '<<|>>'))
  'no HTML comment'                      = (-not ($saved -match '<!--'))
  'no placeholder image'                 = (-not ($saved -match 'placehold\.co|source\.unsplash'))
}
foreach ($k in $checks.Keys) {
  Write-Host ("  {0,-38} {1}" -f $k, $(if ($checks[$k]) { 'PASS' } else { 'FAIL' }))
}

Write-Host ''
Write-Host '--- YOAST PERSISTENCE ---'
$yt = $v.meta.'_yoast_wpseo_title'
$yd = $v.meta.'_yoast_wpseo_metadesc'
$yk = $v.meta.'_yoast_wpseo_focuskw'
Write-Host ("_yoast_wpseo_title    : '{0}'" -f $yt)
Write-Host ("_yoast_wpseo_metadesc : '{0}'" -f $yd)
Write-Host ("_yoast_wpseo_focuskw  : '{0}'" -f $yk)
$yoastOk = -not ([string]::IsNullOrWhiteSpace($yt) -or [string]::IsNullOrWhiteSpace($yd))
Write-Host ("Yoast persisted       : {0}" -f $yoastOk)
if (-not $yoastOk) { Write-Host 'Yoast did NOT persist via REST. Enter title + description in the WP dashboard.' }

Write-Host ''
Write-Host 'REMAINING MANUAL STEPS:'
Write-Host '  1. Open the post in WP Admin and click "Launch Thrive Architect", then Save. Until then the'
Write-Host '     live page renders the semantic HTML fallback (_tve_updated_post is not REST-writable).'
Write-Host '  2. Set the featured image (1309x500) - featured_media was intentionally left unset.'
Write-Host '  3. Add 2-3 body images at 670x352 after the "Which Square deadline" H2, the "Which of your'
Write-Host '     products" H2, and the "What is the right order" H2.'
Write-Host '  4. Confirm Yoast title/description in the dashboard if the check above printed False.'
